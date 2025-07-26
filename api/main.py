from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta

# Try relative imports first, fallback to absolute imports
try:
    from . import models, schemas, crud, recommender, auth
    from .deps import get_db
except ImportError:
    # Fallback for when running directly
    import models, schemas, crud, recommender, auth
    from deps import get_db

app = FastAPI(title="PaiNaiDee API", description="API สำหรับแอป ไปไหนดี")

# Attractions endpoints
@app.get("/attractions", response_model=list[schemas.AttractionOut])
def read_attractions(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """ดึงรายการสถานที่ท่องเที่ยว"""
    return crud.get_attractions(db, skip=skip, limit=limit)

@app.get("/attractions/{attraction_id}", response_model=schemas.AttractionOut)
def read_attraction(attraction_id: int, db: Session = Depends(get_db)):
    """ดึงข้อมูลสถานที่ท่องเที่ยวตาม ID"""
    db_attr = crud.get_attraction(db, attraction_id)
    if not db_attr:
        raise HTTPException(status_code=404, detail="ไม่พบสถานที่ท่องเที่ยว")
    return db_attr

@app.get("/recommend", response_model=list[schemas.AttractionOut])
def recommend(user_id: int, db: Session = Depends(get_db)):
    """แนะนำสถานที่ท่องเที่ยวสำหรับผู้ใช้"""
    return recommender.recommend_for_user(db, user_id)

# Health check endpoint
@app.get("/health")
def health_check():
    """ตรวจสอบสถานะ API"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Root endpoint
@app.get("/")
def root():
    """หน้าแรกของ API"""
    return {
        "message": "ยินดีต้อนรับสู่ PaiNaiDee API",
        "documentation": "/docs",
        "health": "/health"
    }