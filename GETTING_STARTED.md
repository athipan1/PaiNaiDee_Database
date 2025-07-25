# การเริ่มต้นใช้งาน PaiNaiDee Database System

## เริ่ม (Start) - คู่มือเริ่มต้นใช้งาน

ระบบฐานข้อมูล PaiNaiDee พร้อมใช้งานแล้ว! ทำตามขั้นตอนด้านล่างเพื่อเริ่มต้นใช้งาน

### วิธีการเริ่มต้นใช้งาน

#### 1. เริ่มต้นระบบทั้งหมด (แนะนำ)
```bash
python start.py
```
คำสั่งนี้จะ:
- ตรวจสอบและติดตั้ง dependencies
- สร้างฐานข้อมูล SQLite
- เพิ่มข้อมูลตัวอย่าง
- เริ่ม API server ที่ http://127.0.0.1:8000

#### 2. เตรียมระบบเท่านั้น (ไม่รัน server)
```bash
python start.py --init-only
```

#### 3. รันการทดสอบ
```bash
python start.py --test
```

### ตัวเลือกเพิ่มเติม

#### รัน server ที่ host และ port ที่กำหนด
```bash
python start.py --host 0.0.0.0 --port 8080
```

#### รัน server โดยไม่ใช้ auto-reload
```bash
python start.py --no-reload
```

#### ข้ามการเพิ่มข้อมูลตัวอย่าง
```bash
python start.py --skip-sample-data
```

### การใช้งาน API

เมื่อ server เริ่มต้นแล้ว คุณสามารถเข้าถึง:

- **API Documentation**: http://127.0.0.1:8000/docs
- **API Endpoints**:
  - `GET /attractions` - ดูรายการสถานที่ท่องเที่ยว
  - `GET /attractions/{id}` - ดูข้อมูลสถานที่เฉพาะ
  - `GET /recommend?user_id={id}` - รับคำแนะนำสำหรับผู้ใช้

### การตั้งค่าฐานข้อมูล

#### SQLite (เริ่มต้น - สำหรับการพัฒนา)
ระบบจะใช้ SQLite โดยอัตโนมัติ ไฟล์ฐานข้อมูลจะถูกสร้างที่ `./painaidee.db`

#### PostgreSQL (สำหรับการใช้งานจริง)
ตั้งค่าตัวแปรสภาพแวดล้อม:
```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/painaidee_db"
python start.py
```

### การพัฒนาเพิ่มเติม

#### ติดตั้ง dependencies เพิ่มเติม
```bash
pip install -r requirements.txt
```

#### รันตามวิธีเดิม (ตาม README)
```bash
pip install -r requirements.txt
cd api
uvicorn main:app --reload
```

### การแก้ไขปัญหา

#### ปัญหา: Cannot connect to database
- **SQLite**: ตรวจสอบว่ามี permission ในการเขียนไฟล์
- **PostgreSQL**: ตรวจสอบว่า PostgreSQL server กำลังทำงาน

#### ปัญหา: Import errors
ตรวจสอบว่าได้ติดตั้ง dependencies ครบถ้วน:
```bash
python start.py --init-only
```

#### ปัญหา: Port already in use
เปลี่ยน port:
```bash
python start.py --port 8001
```

### ข้อมูลตัวอย่างที่ถูกสร้าง

เมื่อรันคำสั่ง `python start.py` ระบบจะสร้าง:
- ผู้ใช้ตัวอย่าง: `demo_user` (password: `password123`)
- หมวดหมู่: สถานที่ท่องเที่ยว, ร้านอาหาร, ที่พัก, แหล่งช้อปปิ้ง
- แท็ก: สวยงาม, น่าสนใจ, ถ่ายรูปสวย, ครอบครัว
- สถานที่ตัวอย่าง: วัดพระแก้ว

### Files Structure หลังการเริ่มต้น

```
PaiNaiDee_Database/
├── start.py              # สคริปต์เริ่มต้นระบบ
├── painaidee.db          # ไฟล์ฐานข้อมูล SQLite
├── requirements.txt      # Dependencies (อัปเดตแล้ว)
├── api/
│   ├── __init__.py      # Package initialization
│   ├── main.py          # FastAPI application
│   ├── models.py        # Database models
│   ├── schemas.py       # Pydantic schemas (อัปเดตแล้ว)
│   ├── deps.py          # Database dependencies (อัปเดตแล้ว)
│   ├── crud.py          # Database operations
│   └── recommender.py   # Recommendation system
├── tests/
│   └── test_api.py      # API tests
└── scripts/
    ├── fetch_real_data.py
    └── import_export.py
```

## สรุป

ระบบ PaiNaiDee Database พร้อมใช้งานแล้ว! 🎉

เพียงรันคำสั่ง `python start.py` และระบบจะเริ่มต้นอัตโนมัติ พร้อมสำหรับการพัฒนาและทดสอบ