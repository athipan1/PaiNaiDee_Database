from .models import Attraction
from sqlalchemy.orm import Session

def get_attractions(db: Session, skip=0, limit=20):
    return db.query(Attraction).offset(skip).limit(limit).all()

def get_attraction(db: Session, attraction_id: int):
    return db.query(Attraction).filter(Attraction.id == attraction_id).first()