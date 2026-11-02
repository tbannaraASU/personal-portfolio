# Than Bannarat — Portfolio (V15)

เว็บไซต์ Portfolio สำหรับแสดงผลงาน **Software Engineering, Accessibility, Academic Projects และ Photography**

- เว็บไซต์: https://tbannaraasu.github.io/personal-portfolio/
- GitHub: https://github.com/tbannaraASU/personal-portfolio

**สถานะ:** เอกสารนี้อธิบายโค้ด V15; เว็บไซต์ออนไลน์จะเป็น V15 ก็ต่อเมื่อ Merge เข้า `main` และ GitHub Pages Deploy สำเร็จแล้ว

## ความสามารถหลัก

- `index.html`: About, Skills, Featured Projects สูงสุด 3 ชิ้น, Featured Photos สูงสุด 3 รูป, Experience และ Contact
- `projects.html`: ดู Project ทั้งหมด พร้อมกรองตามหมวดหมู่
- `project.html?id=...`: Case Study ที่แสดง Timeline, Role, Skills, Challenge, Approach, Results, Screenshots และลิงก์ที่มีข้อมูลจริง
- `photography.html`, `tag.html`, `album.html`: Collections, Hashtags, Albums และ Gallery ที่เลื่อน Previous/Next ได้ มีลิงก์ Instagram [@foto_4th](https://www.instagram.com/foto_4th/)
- Responsive Design, Dark Mode, WebP Thumbnails, Lazy Loading, Keyboard Navigation และ Project Popups
- Local Admin สำหรับจัดการเนื้อหา โดยไม่ต้องแก้ HTML ทุกครั้ง
- V14 Publisher: Preview ข้อมูลสาธารณะก่อน Push → เปิด PR → เจ้าของ Merge เอง
- V15: Copy Case Study Link, เช็กความครบถ้วนของ Case Studies, SEO Sitemap, Quality Checks, และการรองรับ Cloudflare Web Analytics **แบบปิดไว้ก่อน**

## เปิดระบบ Local บน Mac

```bash
cd ~/ASU/Capstone/GitHub_Competency_Starter
source .venv/bin/activate
python tools/admin_server.py
```

- Portfolio Admin: http://127.0.0.1:8765/admin/portfolio
- Photography Admin: http://127.0.0.1:8765/admin

เมื่อ Save เนื้อหาใน Admin แล้ว ให้ Build (ถ้าระบบไม่ได้ Build ให้ทันที):

```bash
python tools/gallery.py build
python tools/portfolio.py build
```

การแก้เนื้อหาเก็บใน SQLite บน Mac แล้วส่งออกเป็นไฟล์ `data/*.json` และ `data/*-data.js` สำหรับเว็บสาธารณะ **GitHub Pages ไม่รัน Python/SQLite**

## คำสั่งใหม่ V15

```bash
python tools/check_projects_v15.py
python tools/build_sitemap_v15.py
python tools/check_site_v15.py
python tools/cleanup_readmes_v15.py  # Preview คู่มือเก่าที่ลบได้
```

ดูคำแนะนำติดตั้งและ Analytics เพิ่มเติมได้ใน [`README_V15_TH.md`](README_V15_TH.md)

## Publish

- งานแก้ **เนื้อหา/ภาพ**: Save → V14 **Preview changes** → Push & Open PR → Merge เข้า `main`
- งานแก้ **โค้ด/README/Sitemap**: Stage ไฟล์ที่ตั้งใจส่ง, ตรวจ `git diff --cached`, Commit และ Push ใน Feature Branch แล้วสร้าง PR ไป `main`
- V14 Publisher ไม่ได้ Push HTML/CSS/JS/Python ให้เอง และไม่ Merge อัตโนมัติ

## ความปลอดภัย

ห้าม Commit `.env`, `local/`, SQLite, `.venv/`, Secret Tokens, Resume PDF, ไฟล์ข้อมูลส่วนตัว หรือรูปที่ไม่ได้ตั้งใจให้เผยแพร่ ข้อมูล `data/`, Captions, รูป และ Git History ใน Repository สาธารณะอ่านได้ทุกคน

Analytics ของ V15 ยังไม่เก็บสถิติใด ๆ จนกว่าจะใส่ Cloudflare **site token** แล้ว Publish ไฟล์ Configuration และ Merge PR

**Personal AI:** ยังไม่เพิ่ม Demo หรือฟีเจอร์ AI ใหม่ใน V15 และเว็บไซต์ไม่ได้เผยแพร่ Resume PDF
