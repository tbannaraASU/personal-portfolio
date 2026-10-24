# Than Portfolio V9 — Portfolio Content Manager + Project Popup

เว็บนี้ต่อยอดจาก Photography V8 โดย **ไม่เปลี่ยนตาราง/ข้อมูลของแกลเลอรีเดิม** เพิ่มระบบจัดการเนื้อหา Portfolio ใน SQLite และ Project Details Popup ที่แสดงจากข้อมูลใน Database (ส่งออกเป็น static JS สำหรับ GitHub Pages)

## เพิ่มใหม่

- **Portfolio Content Manager**: `http://127.0.0.1:8765/admin/portfolio`
- สามารถแก้ไข / เพิ่ม / ลบ / ซ่อน / เรียงลำดับ Content Items ของ Hero, About Me, Skills, Projects, Education & Experience, Photography intro, Contact, Footer
- สร้าง Custom Sections เพิ่มได้ (เช่น Certifications, Awards, Volunteering)
- แก้ heading, subtitle, description, ลำดับและสถานะ Show/Hide ของแต่ละ Section ได้
- คลิกการ์ด **Project** แล้วเปิด Dialog ที่มี Description เพิ่มเติม, Highlights, Skills/Tags และลิงก์
- หน้า Photo Admin เดิมยังใช้งานได้ที่ `/admin` (Albums, Tags, Add Photos)

## Upgrade V8 → V9 บน Mac (แนะนำ: ใช้ไฟล์ Upgrade Only)

1. หยุด Python Server เก่าโดยกด `Control + C` ใน Terminal
2. เช็ก `git status` และสำรองข้อมูล โดยเฉพาะ `local/gallery.sqlite`, โฟลเดอร์ `photos/`, และไฟล์ `index.html` ถ้ามีการแก้เอง
3. ดาวน์โหลดและแตก ZIP **Than_Portfolio_V9_Upgrade_Only.zip** ลง Repository เดิม ไม่ใช่ใช้ Full ZIP ทับทั้งหมด
4. ใน Terminal:

```bash
cd ~/ASU/Capstone/GitHub_Competency_Starter
source .venv/bin/activate
python tools/portfolio.py build
python tools/admin_server.py
```

5. เปิด Chrome/Safari:
   - Admin Portfolio: http://127.0.0.1:8765/admin/portfolio
   - Portfolio: http://127.0.0.1:8765/index.html
   - Photo Admin: http://127.0.0.1:8765/admin
   - Gallery: http://127.0.0.1:8765/photography.html

SQLite เดิมจะถูกเพิ่มเฉพาะตาราง `portfolio_sections` และ `portfolio_items` เมื่อรันครั้งแรก **ไม่ล้าง** `posts`, `photos`, `hashtags`, `albums` ใน SQLite เดิม

**หมายเหตุ**: ตอนใช้งานครั้งแรก โปรแกรมจะนำข้อมูล Portfolio V8 ที่รวมอยู่ใน `tools/portfolio-seed.json` เข้า Database โดยข้อมูลที่แก้เพิ่มเติมใน HTML เก่าหลัง V8 ไม่ได้ย้ายมาให้อัตโนมัติ ควรสำรองก่อนอัปเกรด

## วิธีใช้หน้า Admin

1. ที่ `/admin/portfolio` เลือก Section ทางซ้าย เช่น `Selected projects`
2. ใน **Section settings** สามารถแก้ Heading, Description, Show/Hide, และสลับลำดับ
3. ที่ **Content items** คลิก Edit / Delete / Move หรือ `＋ Add content`
4. ในส่วน Projects ให้ใส่:
   - **Project title**: ชื่อบนการ์ดและใน Popup
   - **Short card summary**: คำอธิบายสั้นบนการ์ด
   - **Full popup description**: รายละเอียดเมื่อคลิกการ์ด
   - **Key achievements / details**: Highlights เพิ่มเติม (เขียนตามความจริง)
   - **Filter categories**: เช่น `software, ai`
   - **Project URL**: ถ้ามี GitHub / Demo
5. กด **Save item** แล้ว Reload หน้า `/index.html` เพื่อดูผลจริง
6. เพิ่มส่วนอื่นได้ในเมนู `＋ Custom section` และเพิ่ม Content ในส่วนใหม่นั้น

ส่วน Hero และ Footer ใช้ Content รายการแรกที่แสดงอยู่เป็นค่าของ Section นั้น หากต้องการแทนที่ ให้ Edit รายการนั้น (ไม่จำเป็นต้องเพิ่มหลายรายการ)

## การทำงานของ Database และ GitHub Pages

```text
Admin (localhost:8765)
      ↓ save
SQLite (local/gallery.sqlite)
      ↓ auto-export
portfolio-data.js + portfolio.json
      ↓ Git commit + push
GitHub Pages → ผู้เข้าชมเปิดดูเท่านั้น
```

เมื่อแก้ข้อความใน Admin ระบบจะส่งออก:
- `data/portfolio.json`
- `data/portfolio-data.js`

ไม่ต้องรัน `portfolio.py build` ทุกครั้ง แต่รันได้เมื่อต้องการสร้างข้อมูลใหม่จาก DB

**ห้าม commit** `local/`, `.venv/`, raw Instagram exports และข้อมูลส่วนตัวที่ไม่ต้องการเผยแพร่. `.gitignore` ป้องกันส่วนใหญ่แล้วแต่ควรตรวจ `git status` ก่อน Commit. ข้อความ/รูปที่เคยเผยแพร่ใน Git history อาจยังคงมีอยู่

การเผยแพร่:
```bash
# หยุด Server หลังแก้ไข และทำบน branch ใหม่จาก main ที่ sync ล่าสุด

git status
git add index.html portfolio.js data/portfolio-data.js data/portfolio.json README_V9_TH.md
git add tools/admin_server.py tools/portfolio.py tools/portfolio_admin.html tools/portfolio-seed.json tools/photo_admin.html
git commit -m "Add portfolio content manager and project details popup"
git push -u origin feature/portfolio-content-manager
```

เปิด Pull Request และ Merge เข้า `main` แล้ว GitHub Pages จะแสดงเนื้อหาตามไฟล์ที่ Push ส่วนการเพิ่ม/แก้ไขผ่าน Admin ยังต้องทำบน Mac; **GitHub Pages ไม่รัน Python หรือ SQLite**.

## Technical details

- SQLite tables: `portfolio_sections`, `portfolio_items` แยกจาก Gallery
- API: GET `/api/portfolio`; POST `/api/portfolio/section/{create,update,delete}`; POST `/api/portfolio/item/{create,update,delete}`; POST `/api/portfolio/move`
- Admin bound to `127.0.0.1`; POST requests require temporary session token generated on each server start
- Only enabled sections/items are published to `data/portfolio*.js/json` (but content committed earlier may remain in Git history)
- Dynamic user-generated text is HTML-escaped and links are checked against supported URL schemes before rendering
- Delete buttons permanently remove SQLite rows; back up your DB before bulk edits
