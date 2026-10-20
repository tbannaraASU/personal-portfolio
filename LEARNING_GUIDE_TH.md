# GitHub Tutorial - คู่มือทำงานจริง

## ก่อนเริ่ม
- ติดตั้ง Git: https://git-scm.com/downloads
- สมัคร/เข้าสู่ระบบ GitHub: https://github.com
- ใช้ VS Code หรือ text editor อื่น
- ดาวน์โหลดโฟลเดอร์ starter นี้แล้วแตก ZIP
- เปลี่ยน milestone ให้ตรงกับโปรเจกต์ของคุณและทำฟังก์ชันใหม่เอง

## Git CLI: เริ่มโปรเจกต์
เปิด Terminal ภายในโฟลเดอร์ `starter` แล้วพิมพ์:

```bash
git --version
git init -b main
git status
git add index.html README.md
git commit -m "Initial version of capstone tracker"
```

ถ้า Git ขอชื่อและอีเมล ให้ตั้งชื่อ/อีเมลที่ต้องการใช้กับ Git ของคุณ:

```bash
git config --global user.name "YOUR NAME"
git config --global user.email "YOUR EMAIL"
```

## ทำเว็บไซต์เวอร์ชันของคุณ
1. แก้ข้อความ title, description และ milestones ใน index.html
2. เปิด index.html ใน browser เพื่อลอง
3. Commit การเปลี่ยนแปลง:

```bash
git add index.html
git commit -m "Customize tracker milestones"
git log --oneline
```

## สร้างฟีเจอร์บน Branch

```bash
git switch -c feature/progress-counter
```

แก้ index.html เพิ่ม JavaScript ที่นับ checkbox ที่ถูกเลือก แล้วอัปเดต % progress
ตรวจสอบด้วย browser ก่อน commit

```bash
git add index.html
git commit -m "Add progress counter"
```

## Push ไป GitHub
1. สร้าง repository ชื่อ `capstone-milestone-tracker` บน GitHub โดยไม่ติ๊ก Create README (เพราะเรามีไฟล์อยู่แล้ว)
2. คัดลอก URL ของ repository ของคุณ

```bash
git remote add origin https://github.com/YOUR_USERNAME/capstone-milestone-tracker.git
git switch main
git push -u origin main
git switch feature/progress-counter
git push -u origin feature/progress-counter
```

3. ที่ GitHub กด Compare & pull request, ตั้งหัวข้อและบรรยายว่าเพิ่มฟีเจอร์อะไร, Create pull request
4. ตรวจ changes แล้ว Merge pull request
5. กลับมาในเครื่องและ sync:

```bash
git switch main
git pull origin main
git log --oneline --graph --all
```

หมายเหตุ: GitHub อาจให้ Sign in ผ่าน browser หรือ credential manager; รหัสผ่านบัญชี GitHub ธรรมดาใช้ยืนยัน push ผ่าน HTTPS ไม่ได้

## ฝึก Merge Conflict เพิ่ม (optional)
ทดลองในไฟล์ notes.txt เพื่อไม่ให้เว็บเสีย โดยเปลี่ยน *บรรทัดเดียวกัน* ใน 2 branches แล้ว merge จากนั้นแก้เครื่องหมาย conflict และ commit การแก้ไข (เรียนรู้จากวิดีโอส่วน 24:07)

## เก็บหลักฐานที่เป็นของจริง
1. Screenshot เว็บไซต์ที่คุณสร้างสำเร็จ
2. หน้า Commits ของ repository
3. หน้า Pull request ที่แสดง Merged
4. จด log เวลาจริง: เริ่ม-จบ, สิ่งที่ทำ, ปัญหาที่พบ, วิธีแก้

## สิ่งที่ต้องปรับในรายงานก่อนส่ง
- Replace ทุกข้อความใน [square brackets]
- เล่าเฉพาะสิ่งที่ลงมือทำจริง
- เพิ่ม URL repository จริง
- แนบ screenshots ขนาดอ่านได้ พร้อม caption และคำอธิบายในเนื้อหา
- ส่ง PDF ที่จัดตาม template ของ Canvas (หากดาวน์โหลดได้)
