# CI/CD Pipeline Usage Guide

## เริ่มใช้งาน CI/CD Pipeline

### 1. การตั้งค่าเริ่มต้น

```bash
# Clone repository และสร้าง branch ใหม่
git clone <repository-url>
cd PaiNaiDee_Database
git checkout -b feature/your-feature

# ทำการเปลี่ยนแปลง
# ... edit files ...

# Commit และ push
git add .
git commit -m "Your changes"
git push origin feature/your-feature
```

### 2. การทำงานของ CI/CD Pipeline

เมื่อคุณ push หรือสร้าง Pull Request, Pipeline จะทำงานดังนี้:

#### ✅ Setup and Test Job
- ติดตั้ง Python 3.11 และ dependencies
- เริ่ม PostgreSQL service
- ตรวจสอบ code style ด้วย flake8 และ black
- รัน tests ทั้งหมดพร้อม coverage reporting

#### 🗄️ Database Migration Job  
- ตรวจสอบ Alembic migrations
- ทดสอบ database schema
- ตรวจสอบ data population scripts

#### 🚀 Deployment Jobs
- **Staging**: Deploy อัตโนมัติเมื่อ push ไปยัง `develop` branch
- **Production**: Deploy อัตโนมัติเมื่อ push ไปยัง `main` branch

#### 📢 Notification Job
- ส่งแจ้งเตือนผลลัพธ์ของ pipeline
- แสดงสถานะ deployment

### 3. การตรวจสอบผลลัพธ์

1. ไปที่ GitHub repository
2. คลิกที่แท็บ "Actions"
3. ดูผลลัพธ์ของ workflow run

### 4. การแก้ไขเมื่อ Pipeline ล้มเหลว

#### ถ้า Test ล้มเหลว:
```bash
# รัน tests ใน local
pytest tests/ -v

# แก้ไขปัญหาและ commit ใหม่
git add .
git commit -m "Fix tests"
git push
```

#### ถ้า Code Quality ล้มเหลว:
```bash
# ตรวจสอบ linting issues
flake8 .

# แก้ไข formatting
black .

# Commit และ push
git add .
git commit -m "Fix code quality"
git push
```

### 5. การ Deploy

#### Staging Deployment:
- Push ไปยัง `develop` branch
- Pipeline จะ deploy ไปยัง staging environment อัตโนมัติ

#### Production Deployment:
- สร้าง Pull Request ไปยัง `main` branch
- หลังจาก merge, Pipeline จะ deploy ไปยัง production อัตโนมัติ

### 6. Environment Variables

สำหรับ production deployment ให้ตั้งค่า GitHub Secrets:

```
DATABASE_URL=postgresql://user:pass@host:port/db
SECRET_KEY=your-secret-key
ENVIRONMENT=production
```

### 7. การ Monitor

- ตรวจสอบ GitHub Actions logs
- ดู coverage reports
- ติดตาม deployment status

---

**หมายเหตุ**: Pipeline นี้ออกแบบมาเพื่อให้การพัฒนาและ deployment เป็นไปอย่างราบรื่นและปลอดภัย