# PaiNaiDee_Database

ระบบฐานข้อมูลและ API สำหรับแอป "ไปไหนดี"
- FastAPI REST API
- รองรับ JWT Auth
- นำเข้า/ส่งออกข้อมูล
- Recommendation
- เอกสาร API: `/docs`
- ทดสอบ: `pytest`

## เริ่มต้น

### ใช้งานกับ Docker (แนะนำ)
```bash
# สร้างและรันบริการทั้งหมด (backend + PostgreSQL)
docker compose up

# รันในพื้นหลัง
docker compose up -d

# หยุดบริการ
docker compose down
```

### ใช้งานปกติ
```bash
pip install -r requirements.txt
cd api
uvicorn main:app --reload
```

## การใช้งาน
- API endpoint: `http://localhost:5000`
- เอกสาร API: `http://localhost:5000/docs`
- ฐานข้อมูล PostgreSQL: `localhost:5432`