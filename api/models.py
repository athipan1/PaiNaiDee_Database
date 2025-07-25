from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "User"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    avatar_url = Column(String)
    role = Column(String, default="user")

    reviews = relationship("Review", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")


class Category(Base):
    __tablename__ = "Category"
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    icon_url = Column(String)

    attractions = relationship("Attraction", back_populates="category_obj")


class Tag(Base):
    __tablename__ = "Tag"
    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    attraction_tags = relationship("AttractionTag", back_populates="tag")


class Attraction(Base):
    __tablename__ = "attractions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    address = Column(String)
    province = Column(String)
    district = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    category_id = Column(Integer, ForeignKey("Category.category_id"))
    opening_hours = Column(String)
    entrance_fee = Column(String)
    contact_phone = Column(String)
    website = Column(String)
    main_image_url = Column(String)

    category_obj = relationship("Category", back_populates="attractions")
    images = relationship("Image", back_populates="attraction")
    reviews = relationship("Review", back_populates="attraction")
    favorites = relationship("Favorite", back_populates="attraction")
    attraction_tags = relationship("AttractionTag", back_populates="attraction")


class Image(Base):
    __tablename__ = "Image"
    id = Column(Integer, primary_key=True, autoincrement=True)
    attraction_id = Column(Integer, ForeignKey("attractions.id"), nullable=False)
    image_url = Column(String, nullable=False)
    caption = Column(String)

    attraction = relationship("Attraction", back_populates="images")


class Review(Base):
    __tablename__ = "Review"
    id = Column(Integer, primary_key=True, autoincrement=True)
    attraction_id = Column(Integer, ForeignKey("attractions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    attraction = relationship("Attraction", back_populates="reviews")
    user = relationship("User", back_populates="reviews")


class Favorite(Base):
    __tablename__ = "Favorite"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=False)
    attraction_id = Column(Integer, ForeignKey("attractions.id"), nullable=False)
    __table_args__ = (UniqueConstraint('user_id', 'attraction_id', name='_user_attraction_uc'),)

    user = relationship("User", back_populates="favorites")
    attraction = relationship("Attraction", back_populates="favorites")


class AttractionTag(Base):
    __tablename__ = "attraction_tags"
    attraction_id = Column(Integer, ForeignKey("attractions.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("Tag.tag_id"), primary_key=True)
    __table_args__ = (UniqueConstraint('attraction_id', 'tag_id', name='_attraction_tag_uc'),)

    attraction = relationship("Attraction", back_populates="attraction_tags")
    tag = relationship("Tag", back_populates="attraction_tags")
