#!/usr/bin/env python3
"""Update published macro results from US Bureau of Labor Statistics, no API key.

This is a daily *release actuals* update, NOT a consensus provider or real-time quote.
Only tag an event when the BLS observation for that specific month exists AND
its scheduled release time is in the past. Historical BLS revisions may occur.
"""
import datetime as dt
import json
import os
import pathlib
import urllib.request
from decimal import Decimal

ROOT = pathlib.Path(__file__).resolve().parent
OUTPUT = ROOT / 'auto_data.json'
EVENTS = ROOT / 'events.json'
API = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
SERIES = {
    'cpi': 'CUUR0000SA0',   # CPI-U all items, not seasonally adjusted
    'core_cpi': 'CUUR0000SA0L1E', # CPI-U all items less food & energy (NSA)
    'payroll': 'CES0000000001', # total nonfarm payroll, seasonally adjusted, thousands
    'unemployment': 'LNS14000000', # unemployment rate, seasonally adjusted
}
EVENT_MAP = {
    'cpi-oct': ('cpi','2026-10'),
    'cpi-nov': ('cpi','2026-11'),
    'nfp-oct': ('jobs','2026-10'),
    'nfp-nov': ('jobs','2026-11'),
}

def get_series(series_id, startyear, endyear):
    url = f'{API}{series_id}?startyear={startyear}&endyear={endyear}'
    req = urllib.request.Request(url, headers={'User-Agent':'MarketRadar/1.0 (public BLS data)'})
    with urllib.request.urlopen(req, timeout=20) as res:
        body = json.load(res)
    if body.get('status') != 'REQUEST_SUCCEEDED':
        raise RuntimeError(f'BLS {series_id}: {body.get("message") or body.get("status")}')
    entries = (body.get('Results',{}).get('series') or [{}])[0].get('data') or []
    out = {}
    for item in entries:
        period = item.get('period','')
        if len(period) == 3 and period.startswith('M') and period[1:].isdigit() and 1 <= int(period[1:]) <= 12:
            try: out[f'{item["year"]}-{int(period[1:]):02d}'] = Decimal(item['value'].replace(',',''))
            except (KeyError, ValueError, ArithmeticError): continue
    if not out:
        raise RuntimeError(f'No monthly observations for {series_id}')
    return out

def fmt(value, digits=1):
    return f'{value:.{digits}f}'

def build(series, events, now):
    result = {}
    for e in events:
        if e['id'] not in EVENT_MAP: continue
        kind,month = EVENT_MAP[e['id']]
        release_time = dt.datetime.fromisoformat(e['date'])
        if release_time > now: continue
        year, mo = map(int,month.split('-'))
        prev_year = f'{year-1}-{mo:02d}'
        prev_month = f'{year-1}-{12:02d}' if mo == 1 else f'{year}-{mo-1:02d}'
        if kind == 'cpi' and all(month in series[k] and prev_year in series[k] for k in ['cpi','core_cpi']):
            total = (series['cpi'][month]/series['cpi'][prev_year]-1)*100
            core = (series['core_cpi'][month]/series['core_cpi'][prev_year]-1)*100
            result[e['id']] = {
                'actual':f'CPI {fmt(total)}% YoY · Core CPI {fmt(core)}% YoY',
                'period':month,
                'source':'https://www.bls.gov/cpi/',
                'sourceName':'BLS (CPI-U, NSA; calculated YoY)',
            }
        elif kind == 'jobs' and all(month in series[k] for k in ['payroll','unemployment']) and prev_month in series['payroll']:
            jobs = series['payroll'][month]-series['payroll'][prev_month]
            rate = series['unemployment'][month]
            result[e['id']] = {
                'actual':f'Nonfarm Payrolls {int(jobs):+,}K · ว่างงาน {fmt(rate)}%',
                'period':month,
                'source':'https://www.bls.gov/news.release/empsit.toc.htm',
                'sourceName':'BLS (seasonally adjusted; payroll MoM)',
            }
    return result

def main():
    now = dt.datetime.now(dt.timezone.utc)
    series = {key:get_series(s,2025,2026) for key,s in SERIES.items()}
    events = json.loads(EVENTS.read_text(encoding='utf-8'))
    result = build(series,events,now)
    existing = json.loads(OUTPUT.read_text(encoding='utf-8')) if OUTPUT.exists() else {}
    if existing.get('events') == result:
        print('No new results; preserving previous update timestamp')
        return
    payload = {'source':'U.S. Bureau of Labor Statistics', 'updated_at':now.isoformat(timespec='seconds'), 'events':result,
               'note':'Actuals from BLS monthly observations. CPI YoY and payroll MoM are calculated; series may be revised. Forecast/consensus not provided.'}
    OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Updated',len(result),'event actuals')

if __name__ == '__main__': main()
