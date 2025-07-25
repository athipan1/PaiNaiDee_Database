from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# รองรับทั้ง PostgreSQL และ SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./painaidee.db")

# สร้าง engine ตาม database type
if DATABASE_URL.startswith("sqlite"):
    # สำหรับ SQLite ต้องเพิ่ม check_same_thread=False
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # สำหรับ PostgreSQL หรือ database อื่นๆ
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()