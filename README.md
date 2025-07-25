# PaiNaiDee Database

ระบบฐานข้อมูลและ API สำหรับแอป "ไปไหนดี" (Travel Recommendation System)

## คุณสมบัติ
- FastAPI REST API พร้อมเอกสาร Swagger UI
- รองรับ JWT Authentication
- ระบบนำเข้า/ส่งออกข้อมูล
- ระบบ Recommendation สำหรับสถานที่ท่องเที่ยว
- รองรับฐานข้อมูล PostgreSQL และ SQLite
- เอกสาร API อัตโนมัติ: `/docs`
- ทดสอบด้วย pytest

## การติดตั้ง

### วิธีที่ 1: ใช้ pip
```bash
pip install -r requirements.txt
python run_server.py
```

### วิธีที่ 2: ใช้ conda
```bash
conda env create -f environment.yml
conda activate painaidee_env
python run_server.py
```

## การกำหนดค่าฐานข้อมูล

ใช้ environment variables สำหรับความปลอดภัย:

```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/database_name"
export SECRET_KEY="your-very-long-and-secure-secret-key"
```

หากไม่กำหนด จะใช้ SQLite เป็นค่าเริ่มต้น

## การใช้งาน

1. เริ่มเซิร์ฟเวอร์:
```bash
python run_server.py
```

2. เปิด API Documentation:
```
http://localhost:8000/docs
```

3. ทดสอบ API:
```bash
pytest tests/
```

## API Endpoints

- `GET /attractions` - ดึงรายการสถานที่ท่องเที่ยว
- `GET /attractions/{id}` - ดึงข้อมูลสถานที่ท่องเที่ยวตาม ID
- `GET /recommend?user_id={id}` - แนะนำสถานที่สำหรับผู้ใช้

## โครงสร้างไฟล์

```
├── api/                 # FastAPI application
│   ├── main.py         # Main application
│   ├── models.py       # Database models
│   ├── schemas.py      # Pydantic schemas
│   ├── crud.py         # Database operations
│   ├── deps.py         # Dependencies
│   ├── auth.py         # Authentication
│   └── recommender.py  # Recommendation system
├── tests/              # Test files
├── scripts/            # Utility scripts
├── db_script.py        # Database setup script
├── run_server.py       # Server startup script
└── requirements.txt    # Python dependencies
```

## การพัฒนา

1. ติดตั้ง development dependencies:
```bash
pip install -r requirements.txt
```

2. รัน linting:
```bash
flake8 . --max-line-length=127
```

3. รันการทดสอบ:
```bash
pytest tests/ -v
```

## การนำใช้งาน (Deployment)

แนะนำให้ใช้ environment variables ต่อไปนี้:
- `DATABASE_URL`: URL การเชื่อมต่อฐานข้อมูล
- `SECRET_KEY`: กุญแจสำหรับ JWT authentication