# Portfolio V10 — Project Case Study Popups

อัปเกรดจาก Portfolio V9 เพื่อให้ **Project Card เปิด Popup รายละเอียดแบบเต็ม** และจัดการเนื้อหาทั้งหมดผ่าน Portfolio Admin บน Mac

## ฟีเจอร์ใหม่

- Popup แสดง **Project title, status, timeline, duration, role/team, full description, highlights, skills/technologies, screenshots, GitHub และ Demo**
- สไลด์ภาพตัวอย่างหลายภาพใน Popup พร้อม Next/Previous (รวมคีย์บอร์ด ← →)
- เพิ่ม/ลบรูปผ่าน Admin โดยไม่ต้องแก้ HTML รูปจะแปลงเป็น WebP และตัด EXIF/GPS ก่อนเผยแพร่
- เพิ่มฟิลด์ Project details ใน Portfolio Admin; ค่าเดิมใน SQLite ยังคงอยู่ และช่องที่ว่างจะไม่แสดงใน Popup
- ระบบ Photography / Albums / Tags / Photo Manager ยังคงทำงานเหมือน V9

## ติดตั้งแบบปลอดภัย (Mac, ต้องมี V9 อยู่แล้ว)

**1.** หยุด server เดิมใน Terminal ด้วย `Control+C` และตรวจสถานะ Git ก่อนแก้ไข:

```bash
cd ~/ASU/Capstone/GitHub_Competency_Starter
git status
```

หากมีงานค้างไว้ ให้ Commit หรือสำรองก่อนสลับ Branch ห้ามทับไฟล์ที่แก้เองโดยไม่ได้สำรอง

**2.** สำรองฐานข้อมูลและไฟล์โค้ดปัจจุบัน (ถ้ามีฐานข้อมูล):

```bash
mkdir -p ~/Desktop/portfolio-v9-backup
cp local/gallery.sqlite ~/Desktop/portfolio-v9-backup/gallery.sqlite
cp index.html portfolio.js ~/Desktop/portfolio-v9-backup/
```

**3.** เมื่อ Git clean แล้ว สร้าง Branch สำหรับอัปเกรด:

```bash
git switch main
git pull origin main
git switch -c feature/project-detail-popup
```

**4.** แตก `Than_Portfolio_V10_Project_Details_Upgrade.zip` **ลงใน root ของ Repository เดิม** (ไฟล์ ZIP มีเฉพาะไฟล์โปรแกรมและคู่มือ ไม่รวม SQLite หรือไฟล์ Gallery):

```bash
unzip -oq ~/Downloads/Than_Portfolio_V10_Project_Details_Upgrade.zip -d ~/ASU/Capstone/GitHub_Competency_Starter
```

**5.** เปิด local server:

```bash
source .venv/bin/activate
python tools/portfolio.py build
python tools/admin_server.py
```

Chrome/Safari:
- Portfolio Editor: http://127.0.0.1:8765/admin/portfolio
- Portfolio Site: http://127.0.0.1:8765/index.html
- Photo Gallery: http://127.0.0.1:8765/photography.html

## วิธีเพิ่มรายละเอียดโปรเจกต์

1. ไปที่ `/admin/portfolio` → เลือก **Selected projects** ด้านซ้าย
2. คลิก **Edit** ที่โปรเจกต์ เช่น `Personal Portfolio Website`
3. ใส่ข้อมูลที่คุณทำจริงในช่อง:
   - **Project title, Status** — ชื่อและสถานะ
   - **Short card summary** — ข้อความสั้นบนการ์ด
   - **Full popup description** — ที่มา เป้าหมาย สิ่งที่ทำ วิธีทำ และผลลัพธ์
   - **Key achievements / details** — 1 บรรทัดต่อ 1 Highlight
   - **Timeline** — ช่วงเวลาที่ทำจริง เช่น `Oct 2026 – Present`
   - **Duration** — ช่วงระยะเวลา เช่น `Ongoing` หรือ `3 months` (ระบุเฉพาะที่ทราบจริง)
   - **Your role / team size** — งานที่รับผิดชอบ
   - **Skills & technologies** — คั่นด้วย comma เช่น `HTML, CSS, JavaScript, Git, GitHub`
   - **GitHub Repository URL** — URL ของโปรเจกต์นั้นโดยตรง
   - **Live Demo URL** — ใส่เฉพาะเว็บที่เผยแพร่แล้วจริง
   - **Other project URL** — เอกสาร / วิดีโอ / รายละเอียดเพิ่มเติม (ไม่บังคับ)
4. ใน **Project screenshots** เลือกรูป JPG/PNG/WebP แล้วกด **Upload selected images**; รอข้อความยืนยัน จากนั้นกลับไปที่ **Image captions** เพื่อพิมพ์คำบรรยาย *เรียงบรรทัดให้ตรงกับรูป*
5. คลิก **Save item** (สำคัญ: Upload รูปเพียงอย่างเดียวยังไม่ผูกภาพกับ Project จนกด Save)
6. กลับไปที่ `/index.html` และคลิกการ์ด Project เพื่อทดสอบ Popup

จำกัด **6 ภาพต่อการอัปโหลด, 16 ภาพต่อโปรเจกต์, 10 MB ต่อภาพ**; ภาพปรับให้ด้านยาวไม่เกิน 2,200px, แปลงเป็น `.webp` และลบ EXIF/GPS ในขั้นตอนบันทึก

ลบรูปจาก Project Editor จะลบการอ้างอิงในโปรเจกต์เท่านั้น **ไม่ลบไฟล์บนดิสก์** เพื่อป้องกันการลบไฟล์ที่ยังใช้งานอยู่

## เผยแพร่ GitHub Pages

หลัง Save การเปลี่ยนแปลง Admin จะส่งออกข้อมูลไปยัง:

- `data/portfolio-data.js`
- `data/portfolio.json`
- `project-images/` (รูปภาพที่เพิ่มใหม่)

GitHub Pages อ่านเฉพาะ HTML/JavaScript/JSON/WebP **ไม่รัน Python หรือ SQLite**. ตรวจ `git status` แล้ว Commit เฉพาะไฟล์สำหรับเผยแพร่และเครื่องมือที่เปลี่ยน (อย่าเผยแพร่ฐานข้อมูล `local/gallery.sqlite`, `.venv`, raw Instagram Export):

```bash
git add index.html portfolio.js tools/admin_server.py tools/portfolio_admin.html tools/portfolio-seed.json README_V10_TH.md
git add data/portfolio-data.js data/portfolio.json project-images/
git status --short
git commit -m "Add detailed project popups with screenshots and links"
git push -u origin feature/project-detail-popup
```

เปิด Pull Request จาก Branch นี้ แล้ว Merge เข้า `main` เพื่ออัปเดตเว็บไซต์

## ความเข้ากันได้กับ V9

SQLite V9 ไม่จำเป็นต้อง Migration เพราะ `portfolio_items.content` เป็น JSON; ช่องใหม่ถูกบันทึกใน JSON ปัจจุบันเมื่อกด Save; ข้อมูลเก่าที่ไม่มี `images`, `duration`, `skills`, `role`, `github_url`, `demo_url` ยังแสดงผลได้ โดยใช้ `period`, `tags`, `link` เดิมตามความเหมาะสม ไม่มีการล้าง Photo Albums หรือ Hashtags

หากใช้ V8 หรือต่ำกว่า ต้องอัปเกรดไป V9 ก่อน หรือเริ่มจาก V9 Full Package ที่เคยส่งให้ เพื่อให้มีระบบ Portfolio Content Manager
