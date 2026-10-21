# Market Radar — Q4 2026

เว็บต้นแบบติดตามอีเวนต์หุ้นสหรัฐฯ และ Bitcoin ช่วง 22 ตุลาคม–31 ธันวาคม 2026 (เวลาไทย)

## เริ่มใช้งาน

1. เปิด `index.html` ด้วย Chrome/Safari ได้ทันที (ไม่จำเป็นต้องมีเซิร์ฟเวอร์)
2. ถ้าต้องการทดสอบ PWA/offline ให้ใช้เว็บเซิร์ฟเวอร์ เช่น `python3 -m http.server 8080` และเปิด `http://localhost:8080`
3. ถ้าต้องการลิงก์ถาวร อัปโหลดโฟลเดอร์นี้เข้า GitHub Pages, Netlify หรือ Vercel (ใช้ static website)

## ฟีเจอร์

- Timeline / Calendar ตุลาคม–ธันวาคม 2026
- ค้นหาและกรองประเภทอีเวนต์, ความสำคัญสูง, เดือน และสินทรัพย์
- คำอธิบายเป็นภาษาไทย: ตลาดคาดหวังอะไร, ผลแบบไหนหนุนหรือกดหุ้น
- ดูเวลาไทยและ Countdown
- ปุ่ม ☆ บันทึก Favorites, จด Trade Notes, และกรอก Consensus/Actual ด้วยตัวเอง (เก็บใน localStorage ของแต่ละเบราว์เซอร์)
- Export `.ics` เพิ่มอีเวนต์ลง Google/Apple Calendar
- แชร์ลิงก์ตรงไปยังรายละเอียดอีเวนต์ด้วย `#event=...`
- PWA/Offline cache เมื่อใช้งานผ่าน HTTPS หรือ localhost (เปิดไฟล์ตรงๆ ก็ใช้งานหน้าเว็บได้)
- การแสดงผล Mobile/Desktop และรองรับคีย์บอร์ด

## ความแม่นยำของข้อมูล

- ตรวจแหล่งข้อมูล ณ **22 ต.ค. 2026** จาก Federal Reserve, BLS, BEA, US Census, ECB, BOJ, NYSE และ Investor Relations
- รายการที่ยังไม่ยืนยันโดยบริษัท (เช่น NVDA, MU) เป็น **placeholder** ต้องตรวจสอบอีกครั้ง
- เวลาของงบบางบริษัท / BOJ / ECB เป็นเวลาโดยประมาณ ไม่ใช่เวลาประกาศที่ยืนยัน
- **มีผลจริง CPI/Nonfarm Payrolls แบบอัตโนมัติผ่าน BLS (GitHub Actions ทุกวันทำการหลังเวลาประกาศมาตรฐาน)** แต่ **ยังไม่มีราคาหุ้นสด, Consensus สด, ผลงบหุ้นสด, push notifications หรือ cloud sync ของ Favorites/Notes**
- ตารางกำหนดการยังเป็นแบบตรวจสอบด้วยคน: หากวันประกาศเปลี่ยน ให้แก้ `events.json` และ `data.js` และเผยแพร่ใหม่ (หรือแก้ `build_data.py` แล้วสร้างใหม่)
- GitHub Actions `.github/workflows/update-bls.yml` ซิงก์ผลจริง CPI/Jobs จาก BLS วันจันทร์–ศุกร์ เวลา 22:00 ไทย; ปรับตามความหน่วงของ GitHub Actions และ BLS; อัปเดตไฟล์ `auto_data.json` เฉพาะเมื่อข้อมูลเปลี่ยน
- ผล CPI YoY / การเปลี่ยนแปลง Payroll คำนวณจากอนุกรมข้อมูล BLS และอาจถูกปรับปรุงย้อนหลัง; ไม่แสดงเป็นผลทันที ณ วินาทีประกาศ
- กรณีเปิด `index.html` แบบไฟล์ local browser จะบันทึก notes/favorites ได้ แต่เก็บแยกจากการเปิดเว็บบน URL ของโฮสต์

## ข้อมูลและการปรับแก้

- `sync_bls.py` และ `auto_data.json`: อัปเดตผลจริงที่เผยแพร่แล้วจาก BLS โดยไม่ต้องใช้ API key (อาจไม่อัปเดตในวัน BLS ขัดข้อง)

- `data.js`: ชุดข้อมูลอีเวนต์ที่เว็บใช้งานจริง
- `events.json`: สำเนาชุดข้อมูลสำหรับโปรเจกต์/API ในอนาคต
- `app.js`: UI / search / calendar / storage / export
- `style.css`: ดีไซน์ Responsive
- `manifest.webmanifest`, `sw.js`, `icon.svg`: PWA shell

> ตัวอย่างเงื่อนไขบวก/ลบเป็นการตีความทั่วไป ไม่ใช่การรับประกันราคาหุ้นหรือคำแนะนำลงทุนเฉพาะบุคคล
