# PaiNaiDee_Database

ระบบฐานข้อมูลและ API สำหรับแอป "ไปไหนดี"

## 🚀 CI/CD Pipeline

โปรเจกต์นี้มาพร้อมกับ CI/CD pipeline ที่ครบครันซึ่งรวมถึง:

### ✅ Setup Stage (ขั้นตอนการติดตั้ง)
- ติดตั้ง Python dependencies จาก `requirements.txt`
- ติดตั้ง PostgreSQL database service
- ติดตั้ง development tools (flake8, black, pytest-cov, alembic)

### 🧪 Testing Stage (ขั้นตอนการทดสอบ)
- Linting ด้วย flake8 เพื่อตรวจสอบ syntax errors
- Code formatting check ด้วย black
- รัน unit tests และ integration tests ด้วย pytest
- Code coverage reporting
- Database schema validation

### 🗄️ Database Migration Stage
- ตรวจสอบและรัน Alembic database migrations
- ทดสอบ database population scripts
- Schema integrity checks

### 🚀 Deployment Stage
- **Staging**: Auto-deploy เมื่อ push ไปยัง `develop` branch
- **Production**: Auto-deploy เมื่อ push ไปยัง `main` branch
- Support สำหรับ Docker deployment
- Database migration ที่ปลอดภัย

### 📢 Notification Stage
- แจ้งเตือนเมื่อ workflow สำเร็จ
- แจ้งเตือนเมื่อเกิดข้อผิดพลาด
- Deployment status notifications
- Ready สำหรับ integration กับ Slack, Teams, Discord

## 🛠️ Technology Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (python-jose)
- **Testing**: pytest
- **Migration**: Alembic
- **Code Quality**: flake8, black
- **CI/CD**: GitHub Actions
- **Containerization**: Docker & Docker Compose

## 📋 การใช้งาน

### การติดตั้งแบบ Local Development

```bash
# 1. Clone repository
git clone <repository-url>
cd PaiNaiDee_Database

# 2. สร้าง environment file
cp .env.example .env

# 3. แก้ไข .env ให้เหมาะสม
DATABASE_URL=postgresql://postgres:password@localhost:5432/painaidee_db

# 4. ติดตั้ง dependencies
pip install -r requirements.txt

# 5. เริ่ม PostgreSQL (หรือใช้ Docker Compose)
docker-compose up -d db

# 6. รัน database migrations
alembic upgrade head

# 7. เริ่ม API server
cd api
uvicorn main:app --reload
```

### การใช้งานด้วย Docker

```bash
# เริ่มระบบทั้งหมด
docker-compose up

# API จะพร้อมใช้งานที่ http://localhost:8000
# Documentation ที่ http://localhost:8000/docs
```

### การใช้งาน Deployment Script

```bash
# Full deployment
./scripts/deploy.sh

# เฉพาะ database migration
./scripts/deploy.sh migrate

# เฉพาะการทดสอบ
./scripts/deploy.sh test

# ดู help
./scripts/deploy.sh help
```

## 🧪 การทดสอบ

```bash
# รัน tests ทั้งหมด
pytest

# รัน tests พร้อม coverage
pytest --cov=api --cov-report=html

# รัน specific test file
pytest tests/test_api.py -v

# รัน linting
flake8 .

# ตรวจสอบ code formatting
black --check .
```

## 📁 โครงสร้างโปรเจกต์

```
PaiNaiDee_Database/
├── .github/workflows/
│   └── ci-cd.yml              # GitHub Actions CI/CD pipeline
├── api/
│   ├── main.py               # FastAPI application
│   ├── models.py             # SQLAlchemy models
│   ├── schemas.py            # Pydantic schemas
│   ├── crud.py               # Database operations
│   ├── auth.py               # Authentication
│   ├── deps.py               # Dependencies
│   ├── config.py             # Configuration
│   └── recommender.py        # Recommendation engine
├── tests/
│   ├── test_api.py           # Basic API tests
│   └── test_api_improved.py  # Enhanced CI-ready tests
├── scripts/
│   ├── deploy.sh             # Deployment script
│   ├── fetch_real_data.py    # Data fetching utilities
│   └── import_export.py      # Data import/export tools
├── migrations/               # Alembic database migrations
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── alembic.ini              # Alembic configuration
├── setup.cfg                # Tool configurations
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
└── README.md                # Project documentation
```

## 🔧 Configuration

### Environment Variables

สร้างไฟล์ `.env` จาก `.env.example`:

```bash
DATABASE_URL=postgresql://user:password@host:port/database
ENVIRONMENT=development|staging|production
PORT=8000
WORKERS=4
DB_ECHO=false
POPULATE_TEST_DATA=false
LOG_LEVEL=INFO
```

### CI/CD Configuration

CI/CD pipeline จะทำงานอัตโนมัติเมื่อ:
- Push ไปยัง `main` หรือ `develop` branches
- สร้าง Pull Request ไปยัง `main` หรือ `develop` branches

### Database Migration

```bash
# สร้าง migration ใหม่
alembic revision --autogenerate -m "Description"

# รัน migrations
alembic upgrade head

# ย้อนกลับ migration
alembic downgrade -1
```

## 📊 API Endpoints

- `GET /attractions` - รายการสถานที่ท่องเที่ยว
- `GET /attractions/{id}` - รายละเอียดสถานที่ท่องเที่ยว
- `GET /recommend?user_id={id}` - คำแนะนำสำหรับผู้ใช้
- `GET /docs` - API Documentation (Swagger UI)

## 🤝 การมีส่วนร่วม

1. Fork repository
2. สร้าง feature branch
3. ทำการเปลี่ยนแปลง
4. เขียน tests
5. ตรวจสอบให้ผ่าน CI checks
6. สร้าง Pull Request

## 📞 การติดต่อ

หากมีคำถามหรือปัญหา กรุณาสร้าง issue ใน repository นี้