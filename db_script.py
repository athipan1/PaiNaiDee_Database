import requests
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, ForeignKey, UniqueConstraint
# แก้ไข: เปลี่ยนการ import declarative_base ให้ถูกต้องสำหรับ SQLAlchemy 2.0+
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.sql import func # สำหรับ TIMESTAMP
import random
import datetime # สำหรับสร้างวันที่/เวลาจำลอง
import hashlib # สำหรับ hash รหัสผ่านจำลอง

# กำหนดค่าการเชื่อมต่อฐานข้อมูล PostgreSQL
DB_USER = "postgres"
DB_PASSWORD = "Got0896177698"
DB_HOST = "localhost"  # หรือ "db" ถ้าใช้ใน Docker
DB_PORT = "5432"
DB_NAME = "painaidee_db"

# สร้าง URL การเชื่อมต่อฐานข้อมูล
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# สร้าง Engine สำหรับเชื่อมต่อฐานข้อมูล
engine = create_engine(DATABASE_URL)
# สร้าง Base สำหรับโมเดล declarative
Base = declarative_base()
# สร้าง SessionLocal สำหรับการจัดการ session ฐานข้อมูล
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- SQLAlchemy Models ตาม ER Diagram (ปรับปรุงชื่อตารางและ PK ให้ตรงกับ Schema ของคุณ) ---

class User(Base):
    __tablename__ = "User" # เปลี่ยนจาก "users" เป็น "User"
    user_id = Column(Integer, primary_key=True, autoincrement=True) # แก้ไข: เปลี่ยน 'id' เป็น 'user_id'
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    avatar_url = Column(String)
    role = Column(String, default="user") # เช่น "user", "admin"

    reviews = relationship("Review", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")

class Category(Base):
    __tablename__ = "Category" # เปลี่ยนจาก "categories" เป็น "Category"
    category_id = Column(Integer, primary_key=True, autoincrement=True) # แก้ไข: เปลี่ยน 'id' เป็น 'category_id'
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    icon_url = Column(String)

    attractions = relationship("Attraction", back_populates="category_obj")

class Tag(Base):
    __tablename__ = "Tag" # เปลี่ยนจาก "tags" เป็น "Tag"
    tag_id = Column(Integer, primary_key=True, autoincrement=True) # แก้ไข: เปลี่ยน 'id' เป็น 'tag_id'
    name = Column(String, unique=True, nullable=False)

    attraction_tags = relationship("AttractionTag", back_populates="tag")

class Attraction(Base):
    __tablename__ = "attractions" # ชื่อนี้ตรงกับ schema ของคุณแล้ว
    id = Column(Integer, primary_key=True, autoincrement=True) # รักษานามสกุล 'id' เนื่องจาก schema แสดง 'attractions_id_seq'
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    address = Column(String)
    province = Column(String)
    district = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    category_id = Column(Integer, ForeignKey("Category.category_id")) # อัปเดต FK ให้ชี้ไปที่ 'Category.category_id'
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
    __tablename__ = "Image" # เปลี่ยนจาก "images" เป็น "Image"
    id = Column(Integer, primary_key=True, autoincrement=True) # รักษานามสกุล 'id' เนื่องจาก schema แสดง 'Image_image_id_seq'
    attraction_id = Column(Integer, ForeignKey("attractions.id"), nullable=False) # ชื่อตาราง "attractions" ตรงแล้ว
    image_url = Column(String, nullable=False)
    caption = Column(String)

    attraction = relationship("Attraction", back_populates="images")

class Review(Base):
    __tablename__ = "Review" # เปลี่ยนจาก "reviews" เป็น "Review"
    id = Column(Integer, primary_key=True, autoincrement=True) # รักษานามสกุล 'id' เนื่องจาก schema แสดง 'Review_review_id_seq'
    attraction_id = Column(Integer, ForeignKey("attractions.id"), nullable=False) # ชื่อตาราง "attractions" ตรงแล้ว
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=False) # อัปเดต FK ให้ชี้ไปที่ 'User.user_id'
    rating = Column(Integer, nullable=False) # เช่น 1-5 ดาว
    comment = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    attraction = relationship("Attraction", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

class Favorite(Base):
    __tablename__ = "Favorite" # เปลี่ยนจาก "favorites" เป็น "Favorite"
    id = Column(Integer, primary_key=True, autoincrement=True) # รักษานามสกุล 'id' เนื่องจาก schema แสดง 'Favorite_favorite_id_seq'
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=False) # อัปเดต FK ให้ชี้ไปที่ 'User.user_id'
    attraction_id = Column(Integer, ForeignKey("attractions.id"), nullable=False) # ชื่อตาราง "attractions" ตรงแล้ว

    __table_args__ = (UniqueConstraint('user_id', 'attraction_id', name='_user_attraction_uc'),) # ป้องกันการบันทึกรายการโปรดซ้ำ

    user = relationship("User", back_populates="favorites")
    attraction = relationship("Attraction", back_populates="favorites")

class AttractionTag(Base):
    __tablename__ = "attraction_tags" # ชื่อนี้ตรงกับ schema ของคุณแล้ว
    attraction_id = Column(Integer, ForeignKey("attractions.id"), primary_key=True) # ชื่อตาราง "attractions" ตรงแล้ว
    tag_id = Column(Integer, ForeignKey("Tag.tag_id"), primary_key=True) # อัปเดต FK ให้ชี้ไปที่ 'Tag.tag_id'

    __table_args__ = (UniqueConstraint('attraction_id', 'tag_id', name='_attraction_tag_uc'),) # ป้องกันแท็กซ้ำสำหรับสถานที่เดียวกัน

    attraction = relationship("Attraction", back_populates="attraction_tags")
    tag = relationship("Tag", back_populates="attraction_tags")

# สร้างตารางทั้งหมดในฐานข้อมูล (ถ้ายังไม่มี)
# หมายเหตุ: หากตารางมีอยู่แล้วและมีข้อมูลอยู่แล้ว การรัน create_all() จะไม่สร้างตารางซ้ำ
# และจะไม่เพิ่มคอลัมน์ใหม่ที่เพิ่มเข้ามาในโมเดล SQLAlchemy
# หากคุณพบข้อผิดพลาด "UndefinedColumn" หลังจากรันสคริปต์
# อาจจำเป็นต้องลบตารางที่มีปัญหาในฐานข้อมูลของคุณก่อน (เช่น DROP TABLE "User" CASCADE;)
# เพื่อให้ SQLAlchemy สร้างตารางขึ้นมาใหม่พร้อม schema ที่ถูกต้อง
Base.metadata.create_all(bind=engine)

# --- ฟังก์ชันสำหรับดึงข้อมูลจาก API ---

def fetch_data_from_api(api_url):
    """
    ดึงข้อมูล JSON จาก URL API ที่ระบุ

    Args:
        api_url (str): URL ของ API ที่ต้องการดึงข้อมูล

    Returns:
        list: รายการของข้อมูล JSON ที่ได้จาก API หรือลิสต์ว่างถ้ามีข้อผิดพลาด
    """
    try:
        print(f"กำลังดึงข้อมูลจาก: {api_url}")
        response = requests.get(api_url)
        response.raise_for_status()
        print(f"ดึงข้อมูลสำเร็จจาก: {api_url}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"ข้อผิดพลาดในการดึงข้อมูลจาก API ({api_url}): {e}")
        return []

# --- ฟังก์ชันสำหรับบันทึกข้อมูลลงฐานข้อมูล ---

def save_users_to_db(users_data):
    """บันทึกข้อมูลผู้ใช้ลงในตาราง User"""
    session = SessionLocal()
    saved_count = 0
    skipped_count = 0
    user_ids = [] # เก็บ ID ของผู้ใช้ที่บันทึกสำเร็จ
    try:
        for user_item in users_data:
            username = user_item.get("username")
            email = user_item.get("email")
            if not username or not email:
                print(f"ข้ามผู้ใช้เนื่องจากไม่มี username หรือ email: {user_item}")
                skipped_count += 1
                continue

            # แก้ไข: ค้นหาด้วย user_id แทน id
            existing_user = session.query(User).filter((User.username == username) | (User.email == email)).first()
            if existing_user:
                print(f"ข้ามผู้ใช้ '{username}' หรือ '{email}' เนื่องจากมีอยู่ในฐานข้อมูลแล้ว")
                skipped_count += 1
                user_ids.append(existing_user.user_id) # แก้ไข: ใช้ user_id
                continue

            # สร้างรหัสผ่านจำลองและ hash
            mock_password = f"password_{username}"
            password_hash = hashlib.sha256(mock_password.encode()).hexdigest()

            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                avatar_url=f"https://i.pravatar.cc/150?u={username}", # รูป avatar จำลอง
                role="user"
            )
            session.add(user)
            session.flush() # เพื่อให้ได้ ID ของ user ก่อน commit
            user_ids.append(user.user_id) # แก้ไข: ใช้ user_id
            saved_count += 1
        session.commit()
        print(f"บันทึกผู้ใช้สำเร็จ! บันทึกไป {saved_count} รายการ, ข้ามไป {skipped_count} รายการ")
    except Exception as e:
        session.rollback()
        print(f"ข้อผิดพลาดในการบันทึกผู้ใช้: {e}")
    finally:
        session.close()
    return user_ids

def save_categories_and_tags_to_db(categories_list, tags_list):
    """บันทึกข้อมูลหมวดหมู่และแท็กลงในตาราง Category และ Tag"""
    session = SessionLocal()
    saved_categories_count = 0
    saved_tags_count = 0
    category_ids = {} # เก็บ {name: id}
    tag_ids = {}      # เก็บ {name: id}
    try:
        # บันทึก Categories
        for cat_name in categories_list:
            # แก้ไข: ค้นหาด้วย category_id แทน id
            existing_cat = session.query(Category).filter_by(name=cat_name).first()
            if not existing_cat:
                category = Category(
                    name=cat_name,
                    description=f"หมวดหมู่สำหรับ {cat_name}",
                    icon_url=f"https://example.com/icons/{cat_name.lower().replace(' ', '_')}.png"
                )
                session.add(category)
                session.flush()
                category_ids[cat_name] = category.category_id # แก้ไข: ใช้ category_id
                saved_categories_count += 1
            else:
                category_ids[cat_name] = existing_cat.category_id # แก้ไข: ใช้ category_id

        # บันทึก Tags
        for tag_name in tags_list:
            # แก้ไข: ค้นหาด้วย tag_id แทน id
            existing_tag = session.query(Tag).filter_by(name=tag_name).first()
            if not existing_tag:
                tag = Tag(name=tag_name)
                session.add(tag)
                session.flush()
                tag_ids[tag_name] = tag.tag_id # แก้ไข: ใช้ tag_id
                saved_tags_count += 1
            else:
                tag_ids[tag_name] = existing_tag.tag_id # แก้ไข: ใช้ tag_id

        session.commit()
        print(f"บันทึกหมวดหมู่สำเร็จ: {saved_categories_count} รายการ")
        print(f"บันทึกแท็กสำเร็จ: {saved_tags_count} รายการ")
    except Exception as e:
        session.rollback()
        print(f"ข้อผิดพลาดในการบันทึกหมวดหมู่/แท็ก: {e}")
    finally:
        session.close()
    return category_ids, tag_ids

def save_attractions_and_related_data(attractions_data, all_user_ids, all_category_ids, all_tag_ids):
    """บันทึกข้อมูลสถานที่และข้อมูลที่เกี่ยวข้อง (Image, Review, AttractionTag, Favorite)"""
    session = SessionLocal()
    saved_attractions_count = 0
    skipped_attractions_count = 0
    try:
        for attr_item in attractions_data:
            name = attr_item.get("name")
            if not name:
                print(f"ข้ามสถานที่เนื่องจากไม่มีชื่อ: {attr_item}")
                skipped_attractions_count += 1
                continue

            existing_attraction = session.query(Attraction).filter_by(name=name).first()
            if existing_attraction:
                print(f"ข้ามสถานที่ '{name}' เนื่องจากมีอยู่ในฐานข้อมูลแล้ว")
                skipped_attractions_count += 1
                continue

            # ค้นหา category_id จากชื่อหมวดหมู่
            category_id = all_category_ids.get(attr_item.get("category_name"))
            if not category_id:
                print(f"ข้ามสถานที่ '{name}' เนื่องจากไม่พบหมวดหมู่ '{attr_item.get('category_name')}'")
                skipped_attractions_count += 1
                continue

            attraction = Attraction(
                name=name,
                description=attr_item.get("description"),
                address=attr_item.get("address"),
                province=attr_item.get("province"),
                district=attr_item.get("district"),
                latitude=attr_item.get("latitude"),
                longitude=attr_item.get("longitude"),
                category_id=category_id,
                opening_hours=attr_item.get("opening_hours"),
                entrance_fee=attr_item.get("entrance_fee"),
                contact_phone=attr_item.get("contact_phone"),
                website=attr_item.get("website"),
                main_image_url=attr_item.get("main_image_url")
            )
            session.add(attraction)
            session.flush() # เพื่อให้ได้ ID ของ attraction ก่อน commit

            # --- บันทึก Images สำหรับสถานที่นี้ ---
            for i in range(random.randint(1, 3)): # สร้าง 1-3 รูปภาพต่อสถานที่
                image = Image(
                    attraction_id=attraction.id,
                    image_url=f"https://picsum.photos/seed/{attraction.id}-{i}/800/600",
                    caption=f"ภาพที่ {i+1} ของ {attraction.name}"
                )
                session.add(image)

            # --- บันทึก Reviews สำหรับสถานที่นี้ ---
            if all_user_ids:
                for _ in range(random.randint(0, 5)): # สร้าง 0-5 รีวิวต่อสถานที่
                    random_user_id = random.choice(all_user_ids)
                    review = Review(
                        attraction_id=attraction.id,
                        user_id=random_user_id,
                        rating=random.randint(1, 5),
                        comment=random.choice([
                            "สวยงามมาก!", "ประทับใจสุดๆ", "อาหารอร่อย", "บรรยากาศดี",
                            "คุ้มค่าแก่การมาเยือน", "เฉยๆ", "ไม่ค่อยมีอะไร"
                        ]),
                        created_at=datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))
                    )
                    session.add(review)

            # --- บันทึก Tags สำหรับสถานที่นี้ (AttractionTag) ---
            if all_tag_ids:
                num_tags = random.randint(1, min(3, len(all_tag_ids)))
                selected_tag_names = random.sample(list(all_tag_ids.keys()), num_tags)
                for tag_name in selected_tag_names:
                    tag_id = all_tag_ids[tag_name]
                    attraction_tag = AttractionTag(
                        attraction_id=attraction.id,
                        tag_id=tag_id
                    )
                    session.add(attraction_tag)

            # --- บันทึก Favorites สำหรับสถานที่นี้ (สุ่ม) ---
            if all_user_ids and random.random() < 0.3: # 30% ที่จะมีคนกด Favorite
                random_user_id = random.choice(all_user_ids)
                try:
                    favorite = Favorite(
                        user_id=random_user_id,
                        attraction_id=attraction.id
                    )
                    session.add(favorite)
                except Exception as e:
                    # อาจเกิด UniqueConstraint error ถ้าผู้ใช้คนเดิม favorite สถานที่เดิมซ้ำ
                    print(f"ข้อผิดพลาดในการบันทึก Favorite สำหรับ {attraction.name} โดย User ID {random_user_id}: {e}")

            saved_attractions_count += 1
        session.commit()
        print(f"บันทึกสถานที่และข้อมูลที่เกี่ยวข้องสำเร็จ! บันทึกไป {saved_attractions_count} รายการ, ข้ามไป {skipped_attractions_count} รายการ")
    except Exception as e:
        session.rollback()
        print(f"ข้อผิดพลาดในการบันทึกสถานที่และข้อมูลที่เกี่ยวข้อง: {e}")
    finally:
        session.close()

# --- ฟังก์ชันสำหรับดึงและแสดงข้อมูลจากฐานข้อมูล ---

def get_and_display_data():
    """ดึงและแสดงข้อมูลจากทุกตารางเพื่อตรวจสอบ"""
    session = SessionLocal()
    try:
        print("\n--- ข้อมูลจากตาราง User ---")
        users = session.query(User).all()
        for user in users:
            print(f"ID: {user.user_id}, Username: {user.username}, Email: {user.email}, Role: {user.role}") # แก้ไข: ใช้ user_id
        if not users: print("ไม่มีข้อมูลผู้ใช้")

        print("\n--- ข้อมูลจากตาราง Category ---")
        categories = session.query(Category).all()
        for cat in categories:
            print(f"ID: {cat.category_id}, Name: {cat.name}, Description: {cat.description}") # แก้ไข: ใช้ category_id
        if not categories: print("ไม่มีข้อมูลหมวดหมู่")

        print("\n--- ข้อมูลจากตาราง Tag ---")
        tags = session.query(Tag).all()
        for tag in tags:
            print(f"ID: {tag.tag_id}, Name: {tag.name}") # แก้ไข: ใช้ tag_id
        if not tags: print("ไม่มีข้อมูลแท็ก")

        print("\n--- ข้อมูลจากตาราง attractions ---")
        attractions = session.query(Attraction).all()
        for attr in attractions:
            category_name = attr.category_obj.name if attr.category_obj else "N/A"
            tags_names = ", ".join([at.tag.name for at in attr.attraction_tags])
            print(f"ID: {attr.id}, ชื่อ: {attr.name}, หมวดหมู่: {category_name}, "
                  f"ที่อยู่: {attr.address}, พิกัด: ({attr.latitude}, {attr.longitude}), "
                  f"เวลา: {attr.opening_hours}, ค่าเข้า: {attr.entrance_fee}, "
                  f"เว็บไซต์: {attr.website}, รูปหลัก: {attr.main_image_url}, "
                  f"แท็ก: [{tags_names}]")
        if not attractions: print("ไม่มีข้อมูลสถานที่ท่องเที่ยว")

        print("\n--- ข้อมูลจากตาราง Image ---")
        images = session.query(Image).all()
        for img in images:
            print(f"ID: {img.id}, Attraction ID: {img.attraction_id}, URL: {img.image_url}, Caption: {img.caption}")
        if not images: print("ไม่มีข้อมูลรูปภาพ")

        print("\n--- ข้อมูลจากตาราง Review ---")
        reviews = session.query(Review).all()
        for rev in reviews:
            print(f"ID: {rev.id}, Attraction ID: {rev.attraction_id}, User ID: {rev.user_id}, "
                  f"Rating: {rev.rating}, Comment: {rev.comment[:50]}..., Created: {rev.created_at}")
        if not reviews: print("ไม่มีข้อมูลรีวิว")

        print("\n--- ข้อมูลจากตาราง Favorite ---")
        favorites = session.query(Favorite).all()
        for fav in favorites:
            print(f"ID: {fav.id}, User ID: {fav.user_id}, Attraction ID: {fav.attraction_id}")
        if not favorites: print("ไม่มีข้อมูลรายการโปรด")

        print("\n--- ข้อมูลจากตาราง attraction_tags ---")
        attraction_tags = session.query(AttractionTag).all()
        for at in attraction_tags:
            print(f"Attraction ID: {at.attraction_id}, Tag ID: {at.tag_id}")
        if not attraction_tags: print("ไม่มีข้อมูลแท็กของสถานที่")

        print("\n--------------------------------------")

    except Exception as e:
        print(f"ข้อผิดพลาดในการดึงข้อมูลจากฐานข้อมูล: {e}")
    finally:
        session.close()

# --- Main Execution Logic ---
if __name__ == "__main__":
    # URL ตัวอย่างที่ใช้งานได้จริง
    API_URL_USERS = "https://jsonplaceholder.typicode.com/users"
    API_URL_POSTS = "https://jsonplaceholder.typicode.com/posts"

    # 1. บันทึก Categories และ Tags ล่วงหน้า
    predefined_categories = ["สถานที่ท่องเที่ยว", "ร้านอาหาร", "ที่พัก", "แหล่งช้อปปิ้ง", "ธรรมชาติ", "ประวัติศาสตร์", "วัฒนธรรม", "กิจกรรม"]
    predefined_tags = ["สวยงาม", "สงบ", "น่าสนใจ", "อร่อย", "สะดวกสบาย", "ประวัติศาสตร์", "วัฒนธรรม", "ผจญภัย", "ครอบครัว", "ถ่ายรูปสวย", "เดินป่า", "วิวดี"]
    
    category_name_to_id, tag_name_to_id = save_categories_and_tags_to_db(predefined_categories, predefined_tags)
    
    # 2. ดึงและบันทึก Users
    users_data_raw = fetch_data_from_api(API_URL_USERS)
    all_user_ids = save_users_to_db(users_data_raw)

    # 3. ดึง Posts และแปลงเป็นข้อมูล Attraction พร้อมสร้างข้อมูลจำลอง
    posts_data_raw = fetch_data_from_api(API_URL_POSTS)
    mock_attractions_data = []

    provinces = ["กรุงเทพมหานคร", "เชียงใหม่", "ภูเก็ต", "ชลบุรี", "กาญจนบุรี", "อยุธยา"]
    districts = ["เมือง", "บางรัก", "จอมทอง", "แม่ริม", "ถลาง", "บางละมุง", "ไทรโยค", "พระนครศรีอยุธยา"]
    opening_hours_options = ["เปิด 24 ชั่วโมง", "จ-ศ 9:00-17:00", "ทุกวัน 10:00-20:00", "ปิดวันอังคาร"]
    fees_options = ["ฟรี", "50 บาท", "100 บาท", "200 บาท", "ขึ้นอยู่กับกิจกรรม"]

    for post in posts_data_raw:
        if post.get("title"):
            # สุ่มเลือกหมวดหมู่และแท็กสำหรับสถานที่นี้
            random_category_name = random.choice(predefined_categories)
            
            mock_attractions_data.append({
                "name": post["title"],
                "description": post.get("body", "ไม่มีคำอธิบายสำหรับสถานที่นี้"),
                "address": f"{random.randint(1, 100)} ถ.{random.choice(['สุขุมวิท', 'สีลม', 'รัชดา'])}",
                "province": random.choice(provinces),
                "district": random.choice(districts),
                "latitude": round(random.uniform(-90.0, 90.0), 6),
                "longitude": round(random.uniform(-180.0, 180.0), 6),
                "category_name": random_category_name, # ใช้ชื่อหมวดหมู่เพื่อค้นหา ID
                "opening_hours": random.choice(opening_hours_options),
                "entrance_fee": random.choice(fees_options),
                "contact_phone": f"+66{random.randint(80, 99)}{random.randint(1000000, 9999999)}",
                "website": f"https://www.example.com/attraction/{post['id']}",
                "main_image_url": f"https://picsum.photos/seed/{post['id']}/1200/800"
            })
    print(f"สร้างข้อมูลสถานที่จำลองได้ {len(mock_attractions_data)} รายการ")

    # 4. บันทึก Attractions และข้อมูลที่เกี่ยวข้อง
    if mock_attractions_data and all_user_ids and category_name_to_id and tag_name_to_id:
        save_attractions_and_related_data(mock_attractions_data, all_user_ids, category_name_to_id, tag_name_to_id)
    else:
        print("ไม่สามารถบันทึกข้อมูลสถานที่ได้: ข้อมูลไม่ครบถ้วน (สถานที่, ผู้ใช้, หมวดหมู่, แท็ก)")

    # 5. ดึงและแสดงข้อมูลทั้งหมดจากฐานข้อมูลเพื่อตรวจสอบ
    get_and_display_data()
