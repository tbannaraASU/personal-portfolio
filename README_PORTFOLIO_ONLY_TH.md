# Than Portfolio V11 — Portfolio + Photography ONLY

แพ็กเกจนี้ **ไม่มี Personal AI Demo** และไม่ได้สร้าง/แก้ระบบ AI
- แก้ปุ่ม Previous / Next ให้ดูภาพต่อเนื่องข้าม Photo Sets ภายใน Tag/Album
- รองรับลูกศรคีย์บอร์ดและปัดซ้าย-ขวาบนมือถือ
- เพิ่ม Thumbnail WebP 92 รูป เพื่อลดขนาดไฟล์เริ่มต้นที่แสดงใน Gallery
- ปรับ Project Popup สำหรับมือถือ และปัดดู Screenshot ของโปรเจกต์หลายภาพ
- เพิ่มสคริปต์เติมรายละเอียดที่มีแหล่งอ้างอิงของโปรเจกต์ใน Portfolio **ยกเว้น Personal AI** (เลือกใช้เอง)

## ขั้นตอนติดตั้งบน Mac

1. ที่ Terminal โปรเจกต์เดิมตรวจ `git status` และหยุด Server (`Control+C`) ก่อน
2. สำรองไฟล์ที่กำลังจะถูกแทนที่และ SQLite:

```bash
cd ~/ASU/Capstone/GitHub_Competency_Starter
mkdir -p ~/Desktop/portfolio-v11-backup
cp index.html portfolio.js photography.js photography.css ~/Desktop/portfolio-v11-backup/
cp local/gallery.sqlite ~/Desktop/portfolio-v11-backup/gallery.sqlite
```

3. แตก ZIP จาก Downloads ใน Directory เดิม:

```bash
unzip -oq ~/Downloads/Than_Portfolio_V11_Portfolio_Only.zip -d .
source .venv/bin/activate
python tools/gallery.py build
python tools/portfolio.py build
python tools/admin_server.py
```

4. ทดสอบ `http://127.0.0.1:8765/photography.html` → เลือก Tag/Album → คลิกรูป → Previous/Next และปัดบนมือถือ
5. ทดสอบ `http://127.0.0.1:8765/index.html` → Projects → คลิก Popup → เลื่อนรูปตัวอย่างเมื่อโปรเจกต์มีมากกว่า 1 ภาพ

หากต้องการเพิ่ม Skills/Highlights ของโปรเจกต์ที่มีใน Resume โดย **ไม่แตะ Personal AI** และไม่เขียนทับช่องที่มีข้อมูลแล้ว ให้หยุด Server ชั่วคราวแล้วรัน:

```bash
python tools/enrich_portfolio_projects.py
```

ข้อมูลที่ยังไม่ทราบ (เช่นวันเริ่ม/จบ, Duration จริง, ลิงก์โค้ดของโปรเจกต์อื่น) จะเว้นว่างให้แก้ผ่าน Admin

## ก่อน Push ขึ้น GitHub

อัปเดตข้อมูลสาธารณะใหม่ด้วย `python tools/gallery.py build` และ `python tools/portfolio.py build` แล้ว Stage เฉพาะไฟล์ดังนี้:

```bash
git add index.html portfolio.js photography.js photography.css
git add tools/gallery.py tools/check_public_site.py tools/enrich_portfolio_projects.py
git add photos/thumbs/ project-images/portfolio-original-screenshot.webp
git add data/gallery.json data/gallery-data.js data/portfolio.json data/portfolio-data.js
git diff --cached --name-only
```

อย่า Commit `.venv/`, `local/`, `.sqlite`, Instagram Export หรือ Token และตรวจว่าไฟล์ที่ Stage เป็นข้อมูลที่ยินยอมให้เป็น Public

จากนั้นจึง `git commit -m "Improve portfolio gallery navigation and mobile performance"` และ `git push -u origin <YOUR-CURRENT-BRANCH>` เมื่อแน่ใจว่าชื่อ Branch ตรงกับที่ทำอยู่ แล้ว Merge PR เข้า `main`.

**หมายเหตุ:** หากเคยติดตั้ง V11 ชุดที่มี AI แล้ว Package นี้จะไม่ลบโฟลเดอร์ `personal-ai-demo/` ที่อยู่ในเครื่องโดยอัตโนมัติ; ต้องตรวจว่าไม่ได้ Stage/Push โฟลเดอร์ดังกล่าวแยกต่างหาก

## ตรวจหลังเผยแพร่

```bash
python tools/check_public_site.py https://tbannaraasu.github.io/personal-portfolio/
```

การตรวจ HTTP ไม่ยืนยันว่าปุ่มบนเว็บทำงาน ให้ลองเปิด GitHub Pages ด้วย Browser แล้วคลิก Previous/Next และ Project Popup ด้วย
