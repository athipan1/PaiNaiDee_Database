from pydantic import BaseModel
from typing import Optional


class AttractionOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    province: Optional[str] = None
    district: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    opening_hours: Optional[str] = None
    entrance_fee: Optional[str] = None
    website: Optional[str] = None
    main_image_url: Optional[str] = None

    class Config:
        from_attributes = True
