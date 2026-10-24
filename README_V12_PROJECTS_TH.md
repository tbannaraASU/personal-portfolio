# Portfolio V12 — Featured Projects + Project Case Studies

## สิ่งที่เพิ่ม

- `index.html`: โชว์โปรเจกต์เด่น **สูงสุด 3 ชิ้น** พร้อมปุ่ม **View all projects →** ไปที่ `projects.html`
- `projects.html`: รายการโปรเจกต์ทั้งหมด มีปุ่ม Filter ตาม Tags
- `project.html?id=item-...`: หน้า Case Study แยกของแต่ละโปรเจกต์ มีลิงก์แชร์เฉพาะโปรเจกต์
- หน้า Case Study สามารถแสดง Overview, Problem / Challenge, Approach / Solution, Results / Impact, Highlights, Timeline, Duration, Role, Skills, Images (Previous/Next) และ GitHub / Demo เฉพาะข้อมูลที่มีจริง
- **Quick view popup เดิมยังอยู่** บนหน้าแรก เพื่อไม่ทิ้งฟังก์ชัน V10
- `Local Admin` มีช่อง **Homepage selection (Featured/Not featured)** และช่อง Case Study เพิ่มเติม
- **ไม่เพิ่ม AI Demo, ไม่เพิ่ม Resume PDF, ไม่แก้ฐานข้อมูลหรือรูปภาพ**

## วิธีติดตั้งบน Mac

1. **รันจากโปรเจกต์เดิม** ที่ `~/ASU/Capstone/GitHub_Competency_Starter` 
2. หยุด server ด้วย Ctrl+C
3. สำรองไฟล์ปัจจุบัน:

```bash
cd ~/ASU/Capstone/GitHub_Competency_Starter
mkdir -p ~/Desktop/portfolio-v12-backup/tools
cp index.html portfolio.js ~/Desktop/portfolio-v12-backup/
cp tools/portfolio_admin.html ~/Desktop/portfolio-v12-backup/tools/
cp local/gallery.sqlite ~/Desktop/portfolio-v12-backup/gallery.sqlite
```

4. ดาวน์โหลด `Than_Portfolio_V12_Featured_Case_Studies.zip` ไปที่ `~/Downloads` แล้ว:

```bash
unzip -oq ~/Downloads/Than_Portfolio_V12_Featured_Case_Studies.zip -d .
source .venv/bin/activate
python tools/portfolio.py build
python tools/admin_server.py
```

5. เปิด:
    - หน้าแรก: http://127.0.0.1:8765/index.html
    - ทุกโปรเจกต์: http://127.0.0.1:8765/projects.html
    - Admin: http://127.0.0.1:8765/admin/portfolio

> ZIP นี้ไม่รวม `local/gallery.sqlite`, ไม่รวม `data/`, ไม่รวม `photos/` และไม่แก้ `photography.js` หรือ `photography.css` แต่ทำให้ CSS ของหน้าแรกถูกย้ายไปยัง `portfolio-site.css` ดังนั้นต้องคัดลอกไฟล์ใหม่ทุกไฟล์ในแพ็กเกจให้ครบ

## เลือกโปรเจกต์เด่นบนหน้าแรก

- เปิด Admin > เลือก section **Projects**
- กด Edit ที่โปรเจกต์ที่จะให้โชว์หน้าแรก
- ตั้งค่า `Homepage selection (up to 3)` = **Featured** แล้ว Save
- เลือกโปรเจกต์อื่น ๆ จนครบไม่เกิน 3 โครงการ
- ลำดับแสดงผลจะอิงจากลำดับโปรเจกต์ใน Admin (ใช้ปุ่ม ↑ ↓)
- ถ้าไม่ได้ตั้ง Featured **สักโปรเจกต์** หน้าแรกจะใช้ชุดตัวอย่าง 3 ชิ้นจากข้อมูลเดิม คือ **Personal Portfolio Website**, **Student Discussion Application**, **Studio XE** (หากมีและเปิดเผยแพร่อยู่) เพื่อไม่โปรโมต Personal AI ที่ยังไม่ได้ทำ
- หากเริ่มตั้ง Featured แล้ว จะแสดง **เฉพาะรายการที่เลือก** (สูงสุด 3 ชิ้น)
- หากแก้ไขแล้วไม่เห็นบน GitHub Pages ต้อง Commit + Push + Merge ของไฟล์ Build ที่ถูกสร้างใหม่

## เขียน Project Case Study

ที่ Admin > Projects > Edit ให้กรอก:

| ช่อง | ควรเขียนอะไร |
|---|---|
| Project title | ชื่อโปรเจกต์ |
| Status | Completed / In progress ตามความจริง |
| Short card summary | สรุป 1–2 ประโยค |
| Full project description | อธิบายภาพรวม ไม่ต้องอ้างผลที่ยังไม่เกิด |
| Problem / challenge | ปัญหาที่โปรเจกต์มุ่งแก้ |
| Approach / solution | วิธีแก้ปัญหาและสิ่งที่คุณลงมือทำ |
| Results / impact | ผลลัพธ์ที่ **พิสูจน์ได้จริง** เท่านั้น ปล่อยว่างได้ |
| Key achievements | bullet แต่ละข้อขึ้นบรรทัดใหม่ |
| Timeline / Duration | เช่น Fall 2025 / semester-long |
| Your role / team size | งานที่คุณทำเองและจำนวนสมาชิกถ้ามั่นใจ |
| Skills & technologies | เช่น Java, MVC, Git |
| Project screenshots | ใช้ปุ่ม Upload selected images ของ Admin พร้อม Image captions |
| GitHub / Demo links | เพิ่มเฉพาะลิงก์ที่เปิดใช้งานจริง ไม่ต้องใส่ถ้ายังไม่มี |

**ตัวอย่างจาก Resume (ตรวจและปรับเองให้ตรงกับงาน):**

- **Student Discussion Application**: Java, MVC, CRUD, input validation, Agile teamwork, iterative testing (Fall 2025)
- **Studio XE**: axe-core, eslint-plugin-jsx-a11y, React, TypeScript, keyboard/screen-reader accessibility; WCAG 2.2 AA / VPAT 2.5 (Fall 2026 – Spring 2027; **In progress**)
- **LLM-Based Data Sharing Research**: team of six; study privacy decisions involving personal and third-party data, model confidence, consistency, prompting effects (Fall 2026; **In progress**)
- **Personal Portfolio Website**: HTML, CSS, JavaScript, GitHub, static GitHub Pages, Local Admin + generated data, Photography Gallery

อย่าใส่ผลตัวเลข เช่น `Improved performance by 80%` ถ้ายังไม่ได้วัดจริง

## หลังแก้ใน Admin

```bash
python tools/portfolio.py build
```

แล้วให้ตรวจ `data/portfolio.json` / `data/portfolio-data.js` จากนั้น Stage/Commit/Push และ PR เข้า `main` ตาม Workflow ปัจจุบัน

```bash
git add index.html portfolio.js portfolio-site.css projects.css projects.html project.html projects-pages.js tools/portfolio_admin.html README_V12_PROJECTS_TH.md
git add data/portfolio.json data/portfolio-data.js
git diff --cached --check
git diff --cached --stat
```

ตรวจว่าไม่มี `local/gallery.sqlite`, `.venv/`, `.env`, หรือไฟล์ ZIP ถูก Stage ก่อน Commit หากต้องการอัปเดตเว็บสาธารณะ **Merge เข้า `main` และรอ GitHub Pages Deploy สำเร็จก่อนตรวจออนไลน์**

## ทดสอบ

1. `index.html` ต้องเห็น 3 Featured Projects หรือจำนวนที่คุณเลือกเอง
2. Quick view ใช้ได้ และปุ่ม Read full case study เปิดหน้าแยก
3. View all projects เปิด `projects.html` และ Filter ใช้ได้
4. `project.html?id=...` แสดงข้อมูลที่แก้ผ่าน Admin
5. Screenshots มี Previous/Next เมื่อมากกว่า 1 ภาพ
6. Mobile width ไม่ล้น, Theme Light/Dark ทำงาน, Photography ไม่เปลี่ยน

**ผลการทดสอบในแพ็กเกจนี้:** JavaScript syntax ผ่านด้วย Node.js และตัวจำลอง DOM เบื้องต้นผ่านทั้งหน้าแรก, รายการโปรเจกต์ และหน้ารายละเอียด แต่เบราว์เซอร์แบบอัตโนมัติในสภาพแวดล้อมที่สร้างไฟล์ถูกจำกัด จึงยังต้องทดสอบการคลิกบน Mac ของคุณก่อนเผยแพร่
