from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_
from typing import List, Optional
from .models import (
    User, Category, Tag, Attraction, Image, Review, Favorite, AttractionTag
)
from . import schemas
from .auth import get_password_hash

# User CRUD
def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.user_id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        avatar_url=user.avatar_url,
        role=user.role or "user"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[User]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True

# Category CRUD
def get_category(db: Session, category_id: int) -> Optional[Category]:
    return db.query(Category).filter(Category.category_id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    return db.query(Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate) -> Category:
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category_update: schemas.CategoryUpdate) -> Optional[Category]:
    db_category = get_category(db, category_id)
    if not db_category:
        return None
    
    update_data = category_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int) -> bool:
    db_category = get_category(db, category_id)
    if not db_category:
        return False
    db.delete(db_category)
    db.commit()
    return True

# Tag CRUD
def get_tag(db: Session, tag_id: int) -> Optional[Tag]:
    return db.query(Tag).filter(Tag.tag_id == tag_id).first()

def get_tags(db: Session, skip: int = 0, limit: int = 100) -> List[Tag]:
    return db.query(Tag).offset(skip).limit(limit).all()

def create_tag(db: Session, tag: schemas.TagCreate) -> Tag:
    db_tag = Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def update_tag(db: Session, tag_id: int, tag_update: schemas.TagUpdate) -> Optional[Tag]:
    db_tag = get_tag(db, tag_id)
    if not db_tag:
        return None
    
    update_data = tag_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tag, field, value)
    
    db.commit()
    db.refresh(db_tag)
    return db_tag

def delete_tag(db: Session, tag_id: int) -> bool:
    db_tag = get_tag(db, tag_id)
    if not db_tag:
        return False
    db.delete(db_tag)
    db.commit()
    return True

# Attraction CRUD
def get_attraction(db: Session, attraction_id: int) -> Optional[Attraction]:
    return db.query(Attraction).options(
        joinedload(Attraction.category_obj),
        joinedload(Attraction.attraction_tags).joinedload(AttractionTag.tag)
    ).filter(Attraction.id == attraction_id).first()

def get_attractions(db: Session, skip: int = 0, limit: int = 20) -> List[Attraction]:
    return db.query(Attraction).options(
        joinedload(Attraction.category_obj),
        joinedload(Attraction.attraction_tags).joinedload(AttractionTag.tag)
    ).offset(skip).limit(limit).all()

def create_attraction(db: Session, attraction: schemas.AttractionCreate) -> Attraction:
    # Create attraction without tags first
    attraction_data = attraction.dict(exclude={"tag_ids"})
    db_attraction = Attraction(**attraction_data)
    db.add(db_attraction)
    db.commit()
    db.refresh(db_attraction)
    
    # Add tags if provided
    if attraction.tag_ids:
        for tag_id in attraction.tag_ids:
            attraction_tag = AttractionTag(attraction_id=db_attraction.id, tag_id=tag_id)
            db.add(attraction_tag)
        db.commit()
        db.refresh(db_attraction)
    
    return db_attraction

def update_attraction(db: Session, attraction_id: int, attraction_update: schemas.AttractionUpdate) -> Optional[Attraction]:
    db_attraction = get_attraction(db, attraction_id)
    if not db_attraction:
        return None
    
    update_data = attraction_update.dict(exclude_unset=True, exclude={"tag_ids"})
    for field, value in update_data.items():
        setattr(db_attraction, field, value)
    
    # Update tags if provided
    if attraction_update.tag_ids is not None:
        # Remove existing tags
        db.query(AttractionTag).filter(AttractionTag.attraction_id == attraction_id).delete()
        # Add new tags
        for tag_id in attraction_update.tag_ids:
            attraction_tag = AttractionTag(attraction_id=attraction_id, tag_id=tag_id)
            db.add(attraction_tag)
    
    db.commit()
    db.refresh(db_attraction)
    return db_attraction

def delete_attraction(db: Session, attraction_id: int) -> bool:
    db_attraction = get_attraction(db, attraction_id)
    if not db_attraction:
        return False
    db.delete(db_attraction)
    db.commit()
    return True

def search_attractions(db: Session, search: schemas.AttractionSearch) -> tuple[List[Attraction], int]:
    query = db.query(Attraction).options(
        joinedload(Attraction.category_obj),
        joinedload(Attraction.attraction_tags).joinedload(AttractionTag.tag)
    )
    
    # Apply filters
    if search.keyword:
        keyword_filter = or_(
            Attraction.name.ilike(f"%{search.keyword}%"),
            Attraction.description.ilike(f"%{search.keyword}%"),
            Attraction.address.ilike(f"%{search.keyword}%")
        )
        query = query.filter(keyword_filter)
    
    if search.province:
        query = query.filter(Attraction.province.ilike(f"%{search.province}%"))
    
    if search.district:
        query = query.filter(Attraction.district.ilike(f"%{search.district}%"))
    
    if search.category_id:
        query = query.filter(Attraction.category_id == search.category_id)
    
    if search.tag_ids:
        query = query.join(AttractionTag).filter(AttractionTag.tag_id.in_(search.tag_ids))
    
    # Rating filter (requires subquery)
    if search.min_rating or search.max_rating:
        rating_subq = db.query(
            Review.attraction_id,
            func.avg(Review.rating).label('avg_rating')
        ).group_by(Review.attraction_id).subquery()
        
        query = query.join(rating_subq, Attraction.id == rating_subq.c.attraction_id)
        
        if search.min_rating:
            query = query.filter(rating_subq.c.avg_rating >= search.min_rating)
        if search.max_rating:
            query = query.filter(rating_subq.c.avg_rating <= search.max_rating)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    attractions = query.offset(search.skip).limit(search.limit).all()
    
    return attractions, total

# Review CRUD
def get_review(db: Session, review_id: int) -> Optional[Review]:
    return db.query(Review).options(
        joinedload(Review.user),
        joinedload(Review.attraction)
    ).filter(Review.id == review_id).first()

def get_reviews(db: Session, skip: int = 0, limit: int = 100, attraction_id: Optional[int] = None, user_id: Optional[int] = None) -> List[Review]:
    query = db.query(Review).options(
        joinedload(Review.user),
        joinedload(Review.attraction)
    )
    
    if attraction_id:
        query = query.filter(Review.attraction_id == attraction_id)
    if user_id:
        query = query.filter(Review.user_id == user_id)
    
    return query.offset(skip).limit(limit).all()

def create_review(db: Session, review: schemas.ReviewCreate, user_id: int) -> Review:
    db_review = Review(**review.dict(), user_id=user_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def update_review(db: Session, review_id: int, review_update: schemas.ReviewUpdate) -> Optional[Review]:
    db_review = get_review(db, review_id)
    if not db_review:
        return None
    
    update_data = review_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_review, field, value)
    
    db.commit()
    db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: int) -> bool:
    db_review = get_review(db, review_id)
    if not db_review:
        return False
    db.delete(db_review)
    db.commit()
    return True

# Favorite CRUD
def get_user_favorites(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Favorite]:
    return db.query(Favorite).options(
        joinedload(Favorite.attraction)
    ).filter(Favorite.user_id == user_id).offset(skip).limit(limit).all()

def create_favorite(db: Session, favorite: schemas.FavoriteCreate, user_id: int) -> Optional[Favorite]:
    # Check if favorite already exists
    existing = db.query(Favorite).filter(
        and_(Favorite.user_id == user_id, Favorite.attraction_id == favorite.attraction_id)
    ).first()
    if existing:
        return None
    
    db_favorite = Favorite(user_id=user_id, attraction_id=favorite.attraction_id)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

def delete_favorite(db: Session, user_id: int, attraction_id: int) -> bool:
    db_favorite = db.query(Favorite).filter(
        and_(Favorite.user_id == user_id, Favorite.attraction_id == attraction_id)
    ).first()
    if not db_favorite:
        return False
    db.delete(db_favorite)
    db.commit()
    return True

# Image CRUD
def get_attraction_images(db: Session, attraction_id: int) -> List[Image]:
    return db.query(Image).filter(Image.attraction_id == attraction_id).all()

def create_image(db: Session, image: schemas.ImageCreate) -> Image:
    db_image = Image(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def delete_image(db: Session, image_id: int) -> bool:
    db_image = db.query(Image).filter(Image.id == image_id).first()
    if not db_image:
        return False
    db.delete(db_image)
    db.commit()
    return True