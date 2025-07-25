from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    role: Optional[str] = "user"

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None
    role: Optional[str] = None

class UserOut(UserBase):
    user_id: int
    role: str
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Category schemas
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    icon_url: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    icon_url: Optional[str] = None

class CategoryOut(CategoryBase):
    category_id: int
    
    class Config:
        from_attributes = True

# Tag schemas
class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)

class TagOut(TagBase):
    tag_id: int
    
    class Config:
        from_attributes = True

# Attraction schemas
class AttractionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    address: Optional[str] = None
    province: Optional[str] = None
    district: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    opening_hours: Optional[str] = None
    entrance_fee: Optional[str] = None
    contact_phone: Optional[str] = None
    website: Optional[str] = None
    main_image_url: Optional[str] = None

class AttractionCreate(AttractionBase):
    category_id: int
    tag_ids: Optional[List[int]] = []

class AttractionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    address: Optional[str] = None
    province: Optional[str] = None
    district: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    category_id: Optional[int] = None
    opening_hours: Optional[str] = None
    entrance_fee: Optional[str] = None
    contact_phone: Optional[str] = None
    website: Optional[str] = None
    main_image_url: Optional[str] = None
    tag_ids: Optional[List[int]] = None

class AttractionOut(AttractionBase):
    id: int
    category_id: Optional[int] = None
    category: Optional[CategoryOut] = None
    tags: Optional[List[TagOut]] = []
    avg_rating: Optional[float] = None
    review_count: int = 0
    
    class Config:
        from_attributes = True

# Review schemas
class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    attraction_id: int

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None

class ReviewOut(ReviewBase):
    id: int
    attraction_id: int
    user_id: int
    created_at: datetime
    user: Optional[UserOut] = None
    attraction: Optional[AttractionOut] = None
    
    class Config:
        from_attributes = True

# Favorite schemas
class FavoriteCreate(BaseModel):
    attraction_id: int

class FavoriteOut(BaseModel):
    id: int
    user_id: int
    attraction_id: int
    attraction: Optional[AttractionOut] = None
    
    class Config:
        from_attributes = True

# Image schemas
class ImageBase(BaseModel):
    image_url: str
    caption: Optional[str] = None

class ImageCreate(ImageBase):
    attraction_id: int

class ImageUpdate(BaseModel):
    image_url: Optional[str] = None
    caption: Optional[str] = None

class ImageOut(ImageBase):
    id: int
    attraction_id: int
    
    class Config:
        from_attributes = True

# Search and filter schemas
class AttractionSearch(BaseModel):
    keyword: Optional[str] = None
    province: Optional[str] = None
    district: Optional[str] = None
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None
    min_rating: Optional[float] = Field(None, ge=1, le=5)
    max_rating: Optional[float] = Field(None, ge=1, le=5)
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)

# Response schemas
class PaginatedResponse(BaseModel):
    items: List
    total: int
    skip: int
    limit: int
    has_next: bool
    has_prev: bool