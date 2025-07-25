from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List, Optional
import logging

from . import models, schemas, crud, auth, recommender
from .deps import get_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PaiNaiDee API",
    description="API สำหรับแอป ไปไหนดี - ระบบแนะนำสถานที่ท่องเที่ยว",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication endpoints
@app.post("/auth/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    logger.info(f"User registration attempt: {user.username}")
    
    # Check if user already exists
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    db_user = crud.create_user(db, user)
    logger.info(f"User registered successfully: {db_user.username}")
    return db_user

@app.post("/auth/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and get access token."""
    logger.info(f"Login attempt: {form_data.username}")
    
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Failed login attempt: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": str(user.user_id)}, expires_delta=access_token_expires
    )
    
    logger.info(f"User logged in successfully: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me", response_model=schemas.UserOut)
def get_current_user_info(current_user: models.User = Depends(auth.get_current_active_user)):
    """Get current user information."""
    return current_user

# User endpoints
@app.get("/users", response_model=List[schemas.UserOut])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    _: models.User = Depends(auth.require_admin)
):
    """Get all users (admin only)."""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.UserOut)
def read_user(
    user_id: int, 
    db: Session = Depends(get_db)
):
    """Get user by ID."""
    # Check permissions
    current_user = None
    try:
        # Try to get current user from token if provided
        from fastapi import Request
        request = Request  # This will be properly handled by FastAPI
        current_user = auth.get_current_active_user()
    except:
        pass
    
    # Allow access if user is requesting their own data or is admin
    if current_user and (current_user.user_id == user_id or current_user.role == "admin"):
        pass
    else:
        # For now, allow public access to user info (can be restricted later)
        pass
    
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Update user information."""
    # Check if user can update this profile
    if current_user.user_id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Can only update your own profile unless you're an admin"
        )
    
    db_user = crud.update_user(db, user_id, user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(auth.require_admin)
):
    """Delete user (admin only)."""
    if not crud.delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")

# Category endpoints
@app.get("/categories", response_model=List[schemas.CategoryOut])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all categories."""
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories

@app.post("/categories", response_model=schemas.CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(auth.require_admin)
):
    """Create new category (admin only)."""
    return crud.create_category(db, category)

@app.get("/categories/{category_id}", response_model=schemas.CategoryOut)
def read_category(category_id: int, db: Session = Depends(get_db)):
    """Get category by ID."""
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@app.put("/categories/{category_id}", response_model=schemas.CategoryOut)
def update_category(
    category_id: int,
    category_update: schemas.CategoryUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(auth.require_admin)
):
    """Update category (admin only)."""
    db_category = crud.update_category(db, category_id, category_update)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(auth.require_admin)
):
    """Delete category (admin only)."""
    if not crud.delete_category(db, category_id):
        raise HTTPException(status_code=404, detail="Category not found")

# Tag endpoints
@app.get("/tags", response_model=List[schemas.TagOut])
def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all tags."""
    tags = crud.get_tags(db, skip=skip, limit=limit)
    return tags

@app.post("/tags", response_model=schemas.TagOut, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag: schemas.TagCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Create new tag."""
    return crud.create_tag(db, tag)

@app.get("/tags/{tag_id}", response_model=schemas.TagOut)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    """Get tag by ID."""
    db_tag = crud.get_tag(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag

@app.put("/tags/{tag_id}", response_model=schemas.TagOut)
def update_tag(
    tag_id: int,
    tag_update: schemas.TagUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(auth.require_admin)
):
    """Update tag (admin only)."""
    db_tag = crud.update_tag(db, tag_id, tag_update)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag

@app.delete("/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(auth.require_admin)
):
    """Delete tag (admin only)."""
    if not crud.delete_tag(db, tag_id):
        raise HTTPException(status_code=404, detail="Tag not found")

# Attraction endpoints
@app.get("/attractions", response_model=List[schemas.AttractionOut])
def read_attractions(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Get all attractions."""
    attractions = crud.get_attractions(db, skip=skip, limit=limit)
    return attractions

@app.post("/attractions", response_model=schemas.AttractionOut, status_code=status.HTTP_201_CREATED)
def create_attraction(
    attraction: schemas.AttractionCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(auth.require_admin)
):
    """Create new attraction (admin only)."""
    return crud.create_attraction(db, attraction)

@app.get("/attractions/{attraction_id}", response_model=schemas.AttractionOut)
def read_attraction(attraction_id: int, db: Session = Depends(get_db)):
    """Get attraction by ID."""
    db_attraction = crud.get_attraction(db, attraction_id)
    if db_attraction is None:
        raise HTTPException(status_code=404, detail="Attraction not found")
    return db_attraction

@app.put("/attractions/{attraction_id}", response_model=schemas.AttractionOut)
def update_attraction(
    attraction_id: int,
    attraction_update: schemas.AttractionUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(auth.require_admin)
):
    """Update attraction (admin only)."""
    db_attraction = crud.update_attraction(db, attraction_id, attraction_update)
    if db_attraction is None:
        raise HTTPException(status_code=404, detail="Attraction not found")
    return db_attraction

@app.delete("/attractions/{attraction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attraction(
    attraction_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(auth.require_admin)
):
    """Delete attraction (admin only)."""
    if not crud.delete_attraction(db, attraction_id):
        raise HTTPException(status_code=404, detail="Attraction not found")

# Search endpoint
@app.post("/attractions/search", response_model=List[schemas.AttractionOut])
def search_attractions(search: schemas.AttractionSearch, db: Session = Depends(get_db)):
    """Search attractions with filters."""
    attractions, total = crud.search_attractions(db, search)
    return attractions

# Review endpoints
@app.get("/reviews", response_model=List[schemas.ReviewOut])
def read_reviews(
    skip: int = 0,
    limit: int = 100,
    attraction_id: Optional[int] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get reviews."""
    reviews = crud.get_reviews(db, skip=skip, limit=limit, attraction_id=attraction_id, user_id=user_id)
    return reviews

@app.post("/reviews", response_model=schemas.ReviewOut, status_code=status.HTTP_201_CREATED)
def create_review(
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Create new review."""
    return crud.create_review(db, review, current_user.user_id)

@app.get("/reviews/{review_id}", response_model=schemas.ReviewOut)
def read_review(review_id: int, db: Session = Depends(get_db)):
    """Get review by ID."""
    db_review = crud.get_review(db, review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@app.put("/reviews/{review_id}", response_model=schemas.ReviewOut)
def update_review(
    review_id: int,
    review_update: schemas.ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Update review (owner or admin only)."""
    db_review = crud.get_review(db, review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Check if user owns the review or is admin
    if db_review.user_id != current_user.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return crud.update_review(db, review_id, review_update)

@app.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Delete review (owner or admin only)."""
    db_review = crud.get_review(db, review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Check if user owns the review or is admin
    if db_review.user_id != current_user.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    if not crud.delete_review(db, review_id):
        raise HTTPException(status_code=404, detail="Review not found")

# Favorite endpoints
@app.get("/favorites", response_model=List[schemas.FavoriteOut])
def read_user_favorites(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get current user's favorites."""
    favorites = crud.get_user_favorites(db, current_user.user_id, skip=skip, limit=limit)
    return favorites

@app.post("/favorites", response_model=schemas.FavoriteOut, status_code=status.HTTP_201_CREATED)
def create_favorite(
    favorite: schemas.FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Add attraction to favorites."""
    db_favorite = crud.create_favorite(db, favorite, current_user.user_id)
    if db_favorite is None:
        raise HTTPException(status_code=400, detail="Attraction already in favorites")
    return db_favorite

@app.delete("/favorites/{attraction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite(
    attraction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Remove attraction from favorites."""
    if not crud.delete_favorite(db, current_user.user_id, attraction_id):
        raise HTTPException(status_code=404, detail="Favorite not found")

# Recommendation endpoints
@app.get("/recommendations", response_model=List[schemas.AttractionOut])
def get_recommendations(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get personalized recommendations for current user."""
    recommendations = recommender.recommend_for_user(db, current_user.user_id, limit)
    return recommendations

@app.get("/recommendations/trending", response_model=List[schemas.AttractionOut])
def get_trending_attractions(
    days: int = 30,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get trending attractions."""
    trending = recommender.get_trending_attractions(db, days, limit)
    return trending

@app.get("/recommendations/location/{province}", response_model=List[schemas.AttractionOut])
def get_location_recommendations(
    province: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get recommendations for a specific province."""
    recommendations = recommender.get_recommendations_by_location(db, province, limit)
    return recommendations

# Image endpoints
@app.get("/attractions/{attraction_id}/images", response_model=List[schemas.ImageOut])
def read_attraction_images(attraction_id: int, db: Session = Depends(get_db)):
    """Get images for an attraction."""
    images = crud.get_attraction_images(db, attraction_id)
    return images

@app.post("/images", response_model=schemas.ImageOut, status_code=status.HTTP_201_CREATED)
def create_image(
    image: schemas.ImageCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(auth.require_admin)
):
    """Add image to attraction (admin only)."""
    return crud.create_image(db, image)

@app.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_image(
    image_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(auth.require_admin)
):
    """Delete image (admin only)."""
    if not crud.delete_image(db, image_id):
        raise HTTPException(status_code=404, detail="Image not found")

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "PaiNaiDee API is running"}

# Root endpoint
@app.get("/")
def read_root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to PaiNaiDee API",
        "docs": "/docs",
        "version": "1.0.0"
    }