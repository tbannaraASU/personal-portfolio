# Portfolio V13 — Featured Photography, Mobile & Finishing

แพ็กเกจนี้เป็น **patch สำหรับเว็บไซต์ Portfolio V12** ไม่ใช่เว็บใหม่ และไม่รวมฐานข้อมูล `local/gallery.sqlite`, รูปภาพจริง, `data/gallery.json`, Resume, หรือ Personal AI Demo

## การเปลี่ยนแปลง

- **Featured Photo ใน Local Photography Admin**: แสดงรายการรูปทั้งหมดจาก SQLite, คลิกเลือกรูปได้สูงสุด 3 รูป พร้อมแสดงลำดับ 1–3; คลิกอีกครั้งเพื่อลบ; ต้องกด **Save featured photos** จึงจะบันทึกจริง
- เก็บตัวเลือกในตาราง SQLite `featured_photos` ที่สร้างอัตโนมัติเมื่อเปิด Admin/สั่ง Build ไม่แก้หรือลบตารางโพสต์/อัลบั้มเดิม
- หน้าแรก `index.html` แสดงรูปที่เลือกในส่วน Photography พร้อมลิงก์ไปหน้า Gallery และใช้ WebP Preview (พร้อม fallback JPG), `loading="lazy"`, `decoding="async"`
- เมนูมือถือสำหรับหน้าแรก Projects, Project detail, Photography, Album, Tag; ควบคุมด้วยปุ่ม Menu, ปิดด้วย Escape, และรองรับ `aria-expanded`
- Project Cards, Project Dialog, Gallery Viewer และภาพบนมือถือมีการปรับ CSS ลดโอกาสล้นจอและเพิ่มขนาดปุ่มสัมผัส
- เพิ่ม `assets/favicon.svg`, PNG favicon/Apple icon, OG image ขนาด 1200 × 630, Meta Description, Open Graph และ Twitter cards ให้หน้าหลัก ๆ รวมทั้งหน้า `404.html` แบบปรับธีม
- ป้องกันการ Build `gallery.json` ทับเป็น Gallery ว่าง ถ้า SQLite ยังมีโพสต์แต่หาไฟล์รูปต้นฉบับไม่เจอ

## 1. สำรองไฟล์บน Mac ก่อนติดตั้ง

เปิด Terminal:

```bash
cd ~/ASU/Capstone/GitHub_Competency_Starter
mkdir -p ~/Desktop/portfolio-v13-backup/tools
cp index.html portfolio.js portfolio-site.css photography.css ~/Desktop/portfolio-v13-backup/
cp tools/gallery.py tools/admin_server.py tools/photo_admin.html tools/schema.sql ~/Desktop/portfolio-v13-backup/tools/
cp local/gallery.sqlite ~/Desktop/portfolio-v13-backup/gallery.sqlite
```

เก็บสำเนาของไฟล์อื่นที่คุณแก้หลัง V12 เพิ่มเติมด้วย ก่อนแตก ZIP ใหม่นี้ (ZIP จะเขียนทับไฟล์หน้าตา/โค้ดบางส่วน)

## 2. ติดตั้งอัปเกรด

สมมติว่า ZIP อยู่ใน `~/Downloads` และ Terminal อยู่ในโฟลเดอร์ Portfolio แล้ว:

```bash
unzip -oq ~/Downloads/Than_Portfolio_V13_Featured_Photos_Mobile_SEO.zip -d .
source .venv/bin/activate
python tools/gallery.py build
python tools/portfolio.py build
python tools/admin_server.py
```

ถ้าคำสั่ง Build แสดง Gallery เป็น `0 photo sets` ให้หยุดก่อนและตรวจไฟล์ต้นฉบับ JPG ใน `photos/`. แพ็กเกจนี้ **ไม่รวม JPG 92 รูปเดิม** และไม่ควร Import/Replace SQLite เดิมโดยไม่จำเป็น

## 3. เลือก Featured Photos

1. เปิด `http://127.0.0.1:8765/admin`
2. มองหา **★ Featured Photos — Homepage** ที่ด้านบน
3. คลิกภาพ **1 ถึง 3 รูป** ที่ต้องการแสดงหน้าแรก ลำดับที่คลิกเป็นลำดับการแสดง เลือกซ้ำเพื่อนำออก
4. กด **Save featured photos**; ระบบจะ Build `data/gallery.json` และ `data/gallery-data.js` ให้อัตโนมัติ
5. เปิด `http://127.0.0.1:8765/index.html` และเลื่อนลง Photography
6. ลองเมนูมือถือ, หน้ารวม `projects.html`, หน้ารายละเอียด, Album/Tag และ Previous/Next ใน Gallery

**ข้อสำคัญ:** หากเปิดหน้าแรกแล้วไม่เห็นภาพ Featured ให้ตรวจว่ากด Save สำเร็จ และ `python tools/gallery.py build` ไม่รายงาน 0 photo sets

## 4. เผยแพร่ GitHub Pages หลังทดสอบผ่าน

หยุด Server ด้วย `Control+C`, ตรวจ Branch ที่ใช้อยู่ แล้วสั่ง:

```bash
git branch --show-current
git status --short

git add index.html projects.html project.html photography.html tag.html album.html 404.html
git add portfolio.js portfolio-site.css photography.css site-ui.js assets/
git add tools/schema.sql tools/gallery.py tools/admin_server.py tools/photo_admin.html
git add data/gallery.json data/gallery-data.js README_V13_TH.md

git diff --cached --check
git diff --cached --stat
```

ตรวจไฟล์ Stage ก่อน Commit ให้แน่ใจว่าไม่มี `local/`, `.venv/`, `.env`, ZIP/ไฟล์ Private, รูปที่ไม่ต้องการเปิดเผย (และให้รวมรูป WebP/JPG ที่ต้องเผยแพร่หากยังไม่ได้ Commit)

เมื่อมั่นใจแล้วจึง Commit, Push Feature Branch และ Merge Pull Request เข้า `main` ซึ่ง GitHub Pages ใช้เผยแพร่เว็บของคุณ

## 5. ข้อจำกัดที่ควรรู้

- **Local Admin** ใช้แก้ผ่าน Mac เท่านั้น; GitHub Pages ไม่รัน Python/SQLite และไม่ได้อัปเดตตามทันทีจนกว่าจะ Commit/Deploy ไฟล์ที่ Build
- ภาพ Social Preview ตอนแชร์ LinkedIn อาจไม่เปลี่ยนทันที เพราะ LinkedIn อาจ Cache Preview; ต้องตรวจหลัง Deploy และอาจต้อง Refresh ผ่านเครื่องมือตรวจ Post ของ LinkedIn
- Open Graph สำหรับหน้า `project.html?id=...` ใช้ภาพ Preview รวมของ Portfolio เนื่องจาก GitHub Pages เป็น Static Page; ไม่ได้สร้าง OG image รายโปรเจกต์แบบ Server-side
- หากใช้ Custom Domain ในอนาคต ให้แก้ URL แบบ Absolute ของ OG image, canonical ใน `<head>` ให้ตรง Domain ใหม่นั้น
- หากไม่มีการเลือก Featured Photos หน้าแรกจะยังมี Section Photography แบบเดิมพร้อมปุ่มไป Gallery ไม่ใช้รูปสมมติ
- ไม่มีการเพิ่ม Resume PDF หรือ Demo ของ Personal AI ในอัปเกรดนี้

## รายการไฟล์ Patch

`index.html`, `projects.html`, `project.html`, `photography.html`, `tag.html`, `album.html`, `404.html`, `portfolio.js`, `portfolio-site.css`, `photography.css`, `site-ui.js`, `tools/gallery.py`, `tools/admin_server.py`, `tools/photo_admin.html`, `tools/schema.sql`, `assets/*`, และไฟล์คู่มือนี้
