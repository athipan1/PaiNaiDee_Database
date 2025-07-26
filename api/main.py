from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, recommender
from .deps import get_db

app = FastAPI(title="PaiNaiDee API")


@app.get("/attractions", response_model=list[schemas.AttractionOut])
def read_attractions(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_attractions(db, skip=skip, limit=limit)


@app.get("/attractions/{attraction_id}", response_model=schemas.AttractionOut)
def read_attraction(attraction_id: int, db: Session = Depends(get_db)):
    db_attr = crud.get_attraction(db, attraction_id)
    if not db_attr:
        raise HTTPException(status_code=404, detail="Not found")
    return db_attr


@app.get("/recommend", response_model=list[schemas.AttractionOut])
def recommend(user_id: int, db: Session = Depends(get_db)):
    return recommender.recommend_for_user(db, user_id)
