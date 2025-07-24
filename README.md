# PaiNaiDee_Database

ระบบฐานข้อมูลและ API สำหรับแอป "ไปไหนดี"
- FastAPI REST API
- รองรับ JWT Auth
- นำเข้า/ส่งออกข้อมูล
- Recommendation
- เอกสาร API: `/docs`
- ทดสอบ: `pytest`

## เริ่มต้น
```bash
pip install -r requirements.txt
cd api
uvicorn main:app --reload
```