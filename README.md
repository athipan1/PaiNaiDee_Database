# PaiNaiDee Database & API System

ระบบฐานข้อมูลและ API สำหรับแอปพลิเคชัน "ไปไหนดี" (PaiNaiDee) - แพลตฟอร์มแนะนำสถานที่ท่องเที่ยวในประเทศไทย

## 🚀 ฟีเจอร์หลัก

- **FastAPI REST API** - API ที่รวดเร็วและมีประสิทธิภาพ
- **JWT Authentication** - ระบบยืนยันตัวตนที่ปลอดภัย
- **PostgreSQL Database** - ฐานข้อมูลที่เสถียรและรองรับข้อมูลขนาดใหญ่
- **SQLite Testing** - ฐานข้อมูลสำหรับทดสอบ
- **Data Import/Export** - นำเข้าและส่งออกข้อมูล
- **Recommendation System** - ระบบแนะนำสถานที่ท่องเที่ยว
- **API Documentation** - เอกสาร API แบบ interactive ที่ `/docs`
- **Comprehensive Testing** - ระบบทดสอบครอบคลุม

## 📋 ข้อกำหนดระบบ

- Python 3.11+
- PostgreSQL 12+ (สำหรับ production)
- SQLite (สำหรับ development และ testing)

## 🛠️ การติดตั้งและเริ่มใช้งาน

### 1. Clone Repository
```bash
git clone https://github.com/athipan1/PaiNaiDee_Database.git
cd PaiNaiDee_Database
```

### 2. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 3. ทดสอบระบบ
```bash
# ทดสอบการทำงานของ API
python -m pytest tests/ -v

# ทดสอบระบบฐานข้อมูลด้วยข้อมูลตัวอย่าง
TESTING=true python test_database_functionality.py
```

### 4. เริ่มต้น API Server
```bash
cd api
uvicorn main:app --reload
```

หรือ

```bash
# จากไดเรกทอรีหลัก
TESTING=true uvicorn api.main:app --reload --port 8000
```

### 5. เข้าใช้งาน API

- **API Documentation**: http://localhost:8000/docs
- **API Root**: http://localhost:8000/
- **Health Check**: http://localhost:8000/health

## 📖 API Endpoints

### สถานที่ท่องเที่ยว (Attractions)
- `GET /attractions` - ดึงรายการสถานที่ท่องเที่ยว
- `GET /attractions/{id}` - ดึงข้อมูลสถานที่ท่องเที่ยวตาม ID

### ระบบแนะนำ (Recommendations)
- `GET /recommend?user_id={id}` - แนะนำสถานที่ท่องเที่ยวสำหรับผู้ใช้

### ระบบตรวจสอบ (Health Check)
- `GET /health` - ตรวจสอบสถานะ API
- `GET /` - หน้าแรกของ API

## 🗃️ โครงสร้างฐานข้อมูล

### ตารางหลัก
- **users** - ข้อมูลผู้ใช้
- **categories** - หมวดหมู่สถานที่ท่องเที่ยว
- **tags** - แท็กสำหรับจัดหมวดหมู่
- **attractions** - ข้อมูลสถานที่ท่องเที่ยว
- **reviews** - รีวิวและคะแนน
- **favorites** - รายการโปรดของผู้ใช้
- **images** - รูปภาพสถานที่ท่องเที่ยว
- **attraction_tags** - ความสัมพันธ์ระหว่างสถานที่และแท็ก

## 🧪 การทดสอบ

### รันทดสอบ API
```bash
python -m pytest tests/ -v
```

### ทดสอบระบบฐานข้อมูลแบบครอบคลุม
```bash
TESTING=true python test_database_functionality.py
```

### ตัวอย่างผลลัพธ์การทดสอบ
```
🧪 เริ่มทดสอบระบบฐานข้อมูล PaiNaiDee

✅ สร้างตารางสำเร็จ
✅ ลบข้อมูลทดสอบเก่าเรียบร้อย
✅ สร้างข้อมูลตัวอย่างสำเร็จ

📊 สถิติข้อมูล:
   - หมวดหมู่: 4 รายการ
   - แท็ก: 6 รายการ
   - ผู้ใช้: 3 คน
   - สถานที่: 3 แห่ง
   - รีวิว: 3 รีวิว
   - รายการโปรด: 3 รายการ

🎉 การทดสอบเสร็จสิ้น - ระบบฐานข้อมูลทำงานได้ปกติ!
```

## 📁 โครงสร้างโปรเจกต์

```
PaiNaiDee_Database/
├── api/                    # โมดูล API หลัก
│   ├── main.py            # แอปพลิเคชัน FastAPI หลัก
│   ├── models.py          # โมเดลฐานข้อมูล SQLAlchemy
│   ├── schemas.py         # Pydantic schemas
│   ├── crud.py            # ฟังก์ชัน CRUD operations
│   ├── deps.py            # Dependencies และการเชื่อมต่อฐานข้อมูล
│   ├── auth.py            # ระบบยืนยันตัวตน JWT
│   └── recommender.py     # ระบบแนะนำสถานที่
├── tests/                 # ไฟล์ทดสอบ
│   └── test_api.py        # ทดสอบ API endpoints
├── scripts/               # สคริปต์เสริม
│   ├── import_export.py   # นำเข้า/ส่งออกข้อมูล
│   └── fetch_real_data.py # ดึงข้อมูลจาก external APIs
├── db_script.py           # สคริปต์จัดการฐานข้อมูลหลัก
├── test_database_functionality.py  # ทดสอบระบบฐานข้อมูลครอบคลุม
├── requirements.txt       # Python dependencies
├── environment.yml        # Conda environment
└── README.md             # เอกสารนี้
```

## 🔧 การกำหนดค่า

### ตัวแปร Environment
- `DATABASE_URL` - URL การเชื่อมต่อฐานข้อมูล (default: PostgreSQL localhost)
- `TESTING` - ตั้งเป็น `true` เพื่อใช้ SQLite สำหรับทดสอบ

### ตัวอย่าง Database URL
```bash
# PostgreSQL
DATABASE_URL="postgresql://username:password@localhost:5432/database_name"

# SQLite (สำหรับทดสอบ)
DATABASE_URL="sqlite:///./test.db"
```

## 🚀 การใช้งานข้อมูลจริง

### นำเข้าข้อมูลจาก API ภายนอก
```bash
# ทดสอบการดึงข้อมูลจาก TAT API
python scripts/fetch_real_data.py

# รันสคริปต์สร้างข้อมูลตัวอย่าง (ต้องมี PostgreSQL)
python db_script.py
```

### นำเข้า/ส่งออกข้อมูล CSV
```bash
# ในไฟล์ Python
from scripts.import_export import export_users_csv, import_users_csv

# ส่งออกข้อมูลผู้ใช้
export_users_csv("users_backup.csv")

# นำเข้าข้อมูลผู้ใช้
import_users_csv("users_backup.csv")
```

## 🐛 การแก้ไขปัญหา

### ปัญหาการเชื่อมต่อฐานข้อมูล
```bash
# ตรวจสอบว่า PostgreSQL ทำงานอยู่
sudo systemctl status postgresql

# หรือใช้ SQLite สำหรับทดสอบ
TESTING=true uvicorn api.main:app --reload
```

### ปัญหา Import Module
```bash
# เรียกใช้จากไดเรกทอรีหลัก
python -m api.main

# หรือเพิ่ม PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

## 🤝 การพัฒนาและ Contribution

### รันการทดสอบก่อน commit
```bash
python -m pytest tests/ -v
TESTING=true python test_database_functionality.py
```

### โครงสร้างการพัฒนา
1. Fork repository
2. สร้าง feature branch
3. เพิ่มฟีเจอร์และทดสอบ
4. ส่ง Pull Request

## 📝 บันทึกการปรับปรุง

### ✅ ปัญหาที่แก้ไขแล้ว
- ปรับปรุงโครงสร้าง import ให้รองรับทั้ง relative และ absolute imports
- แก้ไขปัญหา Pydantic v2 compatibility
- ทำให้ชื่อตารางในฐานข้อมูลสอดคล้องกัน
- เพิ่ม dependency `httpx` สำหรับการทดสอบ
- ปรับปรุงการจัดการ error และ exception
- เพิ่มระบบทดสอบที่ครอบคลุม
- ปรับปรุงเอกสารและคำแนะนำการใช้งาน

### 🎯 ฟีเจอร์ที่พร้อมใช้งาน
- ✅ FastAPI REST API ทำงานได้ปกติ
- ✅ ระบบฐานข้อมูล SQLAlchemy พร้อมใช้งาน
- ✅ ระบบทดสอบครอบคลุม (7/7 tests passing)
- ✅ API Documentation ที่ `/docs`
- ✅ ระบบแนะนำสถานที่ท่องเที่ยวพื้นฐาน
- ✅ การนำเข้า/ส่งออกข้อมูล
- ✅ Health check endpoints

## 📞 ติดต่อและการสนับสนุน

สำหรับคำถามหรือปัญหาการใช้งาน สามารถ:
- เปิด Issue ใน GitHub Repository
- ตรวจสอบ API Documentation ที่ `/docs`
- ดูตัวอย่างการใช้งานในไฟล์ `test_database_functionality.py`