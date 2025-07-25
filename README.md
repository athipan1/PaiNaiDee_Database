# PaiNaiDee Database & API

ระบบฐานข้อมูลและ API สำหรับแอป "ไปไหนดี" - แพลตฟอร์มแนะนำสถานที่ท่องเที่ยวในประเทศไทย

## 🌟 Features

### Core Features
- 🔐 **JWT Authentication & Role-based Access Control** - ระบบล็อกอินและจัดการสิทธิ์ผู้ใช้
- 🏛️ **Complete CRUD Operations** - จัดการข้อมูลครบครัน (Users, Attractions, Reviews, Favorites, Categories, Tags)
- 🔍 **Advanced Search & Filtering** - ค้นหาสถานที่ตามจังหวัด, แท็ก, หมวดหมู่, คีย์เวิร์ด, คะแนน
- 🤖 **AI-Powered Recommendations** - ระบบแนะนำสถานที่อัจฉริยะ
- 📊 **Data Import/Export** - นำเข้า/ส่งออกข้อมูลในรูปแบบ CSV/JSON
- 📡 **Real Data Integration** - ดึงข้อมูลจากแหล่งจริง (TAT API, Mock APIs)
- 📈 **Logging & Monitoring** - ระบบบันทึกและติดตามการใช้งาน
- 🧪 **Comprehensive Testing** - ครอบคลุมการทดสอบทุกระดับ
- 🚀 **CI/CD Pipeline** - การ deploy อัตโนมัติด้วย GitHub Actions

### API Documentation
- 📖 **Swagger UI**: `/docs`
- 📚 **ReDoc**: `/redoc`
- ❤️ **Health Check**: `/health`

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ 
- PostgreSQL 12+ (หรือ SQLite สำหรับทดสอบ)
- Git

### Installation

1. **Clone Repository**
```bash
git clone https://github.com/athipan1/PaiNaiDee_Database.git
cd PaiNaiDee_Database
```

2. **Setup Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# หรือ
venv\Scripts\activate     # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**
```bash
# สร้างไฟล์ .env
cp .env.example .env

# แก้ไขค่า configuration ใน .env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=painaidee_db
SECRET_KEY=your-secret-key-here
```

5. **Database Setup**
```bash
# สร้างฐานข้อมูล
python db_script.py

# หรือใช้ข้อมูลตัวอย่าง
python scripts/fetch_real_data.py
```

6. **Start API Server**
```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

7. **Access API Documentation**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## 📋 API Endpoints

### Authentication
```
POST   /auth/register     # สมัครสมาชิก
POST   /auth/token        # เข้าสู่ระบบ
GET    /auth/me           # ข้อมูลผู้ใช้ปัจจุบัน
```

### Users
```
GET    /users             # รายชื่อผู้ใช้ทั้งหมด (admin)
GET    /users/{id}        # ข้อมูลผู้ใช้
PUT    /users/{id}        # แก้ไขข้อมูลผู้ใช้
DELETE /users/{id}        # ลบผู้ใช้ (admin)
```

### Categories
```
GET    /categories        # รายชื่อหมวดหมู่
POST   /categories        # สร้างหมวดหมู่ (admin)
GET    /categories/{id}   # ข้อมูลหมวดหมู่
PUT    /categories/{id}   # แก้ไขหมวดหมู่ (admin)
DELETE /categories/{id}   # ลบหมวดหมู่ (admin)
```

### Tags
```
GET    /tags              # รายชื่อแท็ก
POST   /tags              # สร้างแท็ก
GET    /tags/{id}         # ข้อมูลแท็ก
PUT    /tags/{id}         # แก้ไขแท็ก (admin)
DELETE /tags/{id}         # ลบแท็ก (admin)
```

### Attractions
```
GET    /attractions       # รายชื่อสถานที่
POST   /attractions       # สร้างสถานที่ (admin)
GET    /attractions/{id}  # ข้อมูลสถานที่
PUT    /attractions/{id}  # แก้ไขสถานที่ (admin)
DELETE /attractions/{id}  # ลบสถานที่ (admin)
POST   /attractions/search # ค้นหาสถานที่
```

### Reviews
```
GET    /reviews           # รายชื่อรีวิว
POST   /reviews           # เขียนรีวิว
GET    /reviews/{id}      # ข้อมูลรีวิว
PUT    /reviews/{id}      # แก้ไขรีวิว (เจ้าของ/admin)
DELETE /reviews/{id}      # ลบรีวิว (เจ้าของ/admin)
```

### Favorites
```
GET    /favorites         # รายการโปรดของผู้ใช้
POST   /favorites         # เพิ่มรายการโปรด
DELETE /favorites/{id}    # ลบรายการโปรด
```

### Recommendations
```
GET    /recommendations              # แนะนำสำหรับผู้ใช้
GET    /recommendations/trending     # สถานที่ยอดนิยม
GET    /recommendations/location/{province} # แนะนำตามจังหวัด
```

### Images
```
GET    /attractions/{id}/images     # รูปภาพของสถานที่
POST   /images                      # เพิ่มรูปภาพ (admin)
DELETE /images/{id}                 # ลบรูปภาพ (admin)
```

## 🔍 Search Examples

### Basic Search
```json
POST /attractions/search
{
  "keyword": "วัด",
  "province": "กรุงเทพมหานคร",
  "skip": 0,
  "limit": 10
}
```

### Advanced Search
```json
POST /attractions/search
{
  "keyword": "ตลาดน้ำ",
  "province": "สมุทรสาคร",
  "category_id": 1,
  "tag_ids": [1, 3, 5],
  "min_rating": 4.0,
  "max_rating": 5.0,
  "skip": 0,
  "limit": 20
}
```

## 🤖 Recommendation System

ระบบแนะนำใช้อัลกอริทึมที่พิจารณาจาก:

1. **Category-based (40%)** - หมวดหมู่ที่ผู้ใช้ชอบ
2. **Popularity-based (30%)** - ความนิยมของสถานที่
3. **Collaborative Filtering (20%)** - ผู้ใช้ที่มีความชอบคล้ายกัน
4. **Random (10%)** - ความหลากหลาย

## 📊 Data Management

### Export Data
```python
from scripts.import_export import export_all_data

# Export ทุกตารางเป็น JSON
results = export_all_data("json")

# Export เฉพาะ attractions เป็น CSV
from scripts.import_export import export_attractions_csv
filepath = export_attractions_csv("attractions_backup.csv")
```

### Import Data
```python
from scripts.import_export import import_attractions_csv

# Import ข้อมูลจาก CSV
result = import_attractions_csv("attractions_data.csv", update_existing=True)
print(result)
```

### Fetch Real Data
```python
from scripts.fetch_real_data import fetch_tat_data

# ดึงข้อมูลจาก TAT API
result = fetch_tat_data(province="กรุงเทพมหานคร", limit=50)
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=api --cov-report=html

# Run specific test class
pytest tests/test_api.py::TestAuthentication -v

# Run integration tests
pytest tests/ -k "integration" -v
```

### Test Categories
- **Unit Tests** - ทดสอบ functions และ classes แต่ละตัว
- **Integration Tests** - ทดสอบการทำงานร่วมกันของ components
- **API Tests** - ทดสอบ endpoints และ responses
- **Authentication Tests** - ทดสอบระบบล็อกอินและสิทธิ์
- **Data Validation Tests** - ทดสอบการตรวจสอบข้อมูล

## 🚀 Deployment

### Development
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
# ใช้ gunicorn สำหรับ production
pip install gunicorn
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "api.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### Environment Variables
```bash
# Database
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=painaidee_db

# Security
SECRET_KEY=your-super-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Optional
DATABASE_URL=postgresql://user:pass@host:port/db
DEBUG=false
LOG_LEVEL=INFO
```

## 📈 Monitoring & Logging

### Access Logs
API มีระบบ logging ครอบคลุม:
- Request/Response logging
- Error tracking
- Performance metrics
- Authentication attempts

### Health Check
```bash
curl http://localhost:8000/health
```

### Monitoring Endpoints
- `/health` - ตรวจสอบสถานะระบบ
- `/docs` - API documentation
- `/metrics` - Performance metrics (ถ้ามี)

## 🔒 Security Features

- **JWT Authentication** - ระบบ token-based authentication
- **Role-based Access Control** - จัดการสิทธิ์ user/admin
- **Password Hashing** - bcrypt hashing
- **Data Validation** - Pydantic validation
- **SQL Injection Protection** - SQLAlchemy ORM
- **CORS Configuration** - Cross-origin request handling

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Development Guidelines
- ใช้ Black สำหรับ code formatting
- ใช้ flake8 สำหรับ linting
- เขียน tests สำหรับ features ใหม่
- อัปเดต documentation เมื่อมีการเปลี่ยนแปลง

## 📁 Project Structure

```
PaiNaiDee_Database/
├── api/                    # FastAPI application
│   ├── main.py            # Main application
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   ├── crud.py            # Database operations
│   ├── auth.py            # Authentication
│   ├── deps.py            # Dependencies
│   └── recommender.py     # Recommendation system
├── scripts/               # Utility scripts
│   ├── import_export.py   # Data import/export
│   └── fetch_real_data.py # External data fetching
├── tests/                 # Test files
│   └── test_api.py       # API tests
├── .github/workflows/     # CI/CD configuration
│   └── ci.yml            # GitHub Actions
├── db_script.py          # Database initialization
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- 📧 Email: support@painaidee.com
- 🐛 Issues: [GitHub Issues](https://github.com/athipan1/PaiNaiDee_Database/issues)
- 📖 Documentation: [API Docs](http://localhost:8000/docs)

## 🙏 Acknowledgments

- Tourism Authority of Thailand (TAT) สำหรับข้อมูลสถานที่ท่องเที่ยว
- FastAPI community สำหรับ framework ที่ยอดเยี่ยม
- SQLAlchemy และ Pydantic สำหรับเครื่องมือที่มีประสิทธิภาพ

---

**PaiNaiDee** - *Your Ultimate Thailand Travel Companion* 🇹🇭✨