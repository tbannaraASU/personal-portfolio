# Portfolio V13 — Photography Homepage Layout Patch

## ผลลัพธ์

- ใน `index.html` ส่วน Photography จะแสดง **Featured Photos สูงสุด 3 รูปก่อน** (ที่เลือกจาก Local Gallery Admin)
- ถัดลงมาเป็นปุ่ม **See More Photos →** เชื่อมไป `photography.html`
- ไม่แสดงกล่องข้อความ **Curiosity in every frame** / ไอคอนกล้องบนหน้าแรกอีก
- **Featured Photos ยังเลือก เปลี่ยน หรือนำออกได้จาก Local Admin เหมือนเดิม** (`http://127.0.0.1:8765/admin`)
- ถ้าไม่มี Featured Photos ให้แสดงแค่ปุ่ม See More Photos และสามารถกลับมาเลือกเพิ่มทีหลังได้
- ไม่แตะ `local/gallery.sqlite`, `data/gallery.json`, `data/gallery-data.js`, รูปถ่าย หรือหน้า Gallery
- ชื่อและข้อความส่วน Photography ใน Portfolio Admin ยังเก็บไว้ ไม่ถูกลบ เพียงไม่แสดงเป็น banner ที่หน้าแรก

## ติดตั้งบน Mac (ใช้กับ V13)

1. ดาวน์โหลด ZIP แล้ววางไว้ที่ Downloads
2. เปิด Terminal และรัน:

```bash
cd ~/ASU/Capstone/GitHub_Competency_Starter
unzip -oq ~/Downloads/Portfolio_V13_Photo_Layout_Patch.zip -d .
python3 tools/apply_photo_layout_v13.py
python tools/admin_server.py
```

> หากยังไม่ได้ activate `.venv`: `source .venv/bin/activate` ก่อนรัน `python tools/admin_server.py` หรือใช้ `python3 tools/admin_server.py`

3. เปิด `http://127.0.0.1:8765/index.html` แล้ว Refresh แบบไม่ใช้แคช (`Cmd+Shift+R`)
4. ตรวจภาพเด่น 3 รูปอยู่บนปุ่ม See More Photos, คลิกไป Gallery ได้
5. ลองเปลี่ยนภาพจาก `http://127.0.0.1:8765/admin` → **★ Featured Photos — Homepage** → Save
6. เปิด `index.html` อีกครั้งแล้ว Refresh เพื่อตรวจรูปใหม่

สคริปต์จะแก้เฉพาะ `portfolio.js` และ `portfolio-site.css` และเก็บไฟล์เดิมสำรองใน `local/photo-layout-backups/...` อัตโนมัติ โฟลเดอร์ `local/` ถูก ignore จาก Git ในโปรเจกต์ V13

## ก่อนอัปเดต GitHub Pages

```bash
git diff -- portfolio.js portfolio-site.css
git add portfolio.js portfolio-site.css
git diff --cached --check
git status --short
```

หากเลือก Featured Photos ใหม่ด้วย Admin ให้ `git add data/gallery.json data/gallery-data.js` เพิ่มด้วยหลังจากตรวจเนื้อหา

Commit และ Push บน Feature Branch ที่คุณใช้อยู่ แล้วเปิด Pull Request เพื่อ Merge เข้า `main`

## ย้อนกลับ

ใช้ไฟล์ใน `local/photo-layout-backups/<timestamp>/portfolio.js` และ `portfolio-site.css` ที่สคริปต์สำรองไว้ หรือใช้ `git restore` ตามสถานะ Git ของคุณ
