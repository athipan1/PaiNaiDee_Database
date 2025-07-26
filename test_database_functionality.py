#!/usr/bin/env python3
"""
สคริปต์สำหรับทดสอบฟังก์ชันการทำงานของฐานข้อมูล PaiNaiDee
ใช้ข้อมูลจำลองเพื่อทดสอบการสร้าง อ่าน อัปเดต และลบข้อมูล
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.models import Base, User, Category, Tag, Attraction, Review, Favorite, AttractionTag
from api.deps import engine, SessionLocal
import random
from datetime import datetime, timedelta

def create_test_database():
    """สร้างตารางในฐานข้อมูลทดสอบ"""
    print("กำลังสร้างตารางในฐานข้อมูล...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ สร้างตารางสำเร็จ")
        return True
    except Exception as e:
        print(f"❌ ข้อผิดพลาดในการสร้างตาราง: {e}")
        return False

def clear_test_data():
    """ลบข้อมูลทดสอบทั้งหมด"""
    session = SessionLocal()
    try:
        # ลบข้อมูลในลำดับที่ถูกต้อง (เนื่องจาก foreign key constraints)
        session.query(AttractionTag).delete()
        session.query(Favorite).delete()
        session.query(Review).delete()
        session.query(Attraction).delete()
        session.query(Category).delete()
        session.query(Tag).delete()
        session.query(User).delete()
        session.commit()
        print("✅ ลบข้อมูลทดสอบเก่าเรียบร้อย")
    except Exception as e:
        session.rollback()
        print(f"❌ ข้อผิดพลาดในการลบข้อมูล: {e}")
    finally:
        session.close()

def create_sample_data():
    """สร้างข้อมูลตัวอย่าง"""
    session = SessionLocal()
    try:
        print("กำลังสร้างข้อมูลตัวอย่าง...")
        
        # สร้าง Categories
        categories = [
            Category(name="สถานที่ท่องเที่ยว", description="แหล่งท่องเที่ยวทั่วไป"),
            Category(name="ร้านอาหาร", description="ร้านอาหารและเครื่องดื่ม"),
            Category(name="ที่พัก", description="โรงแรมและที่พัก"),
            Category(name="ธรรมชาติ", description="แหล่งท่องเที่ยวธรรมชาติ"),
        ]
        
        for category in categories:
            session.add(category)
        session.flush()
        
        # สร้าง Tags
        tags = [
            Tag(name="สวยงาม"),
            Tag(name="สงบ"),
            Tag(name="อร่อย"),
            Tag(name="ประวัติศาสตร์"),
            Tag(name="ครอบครัว"),
            Tag(name="ถ่ายรูปสวย"),
        ]
        
        for tag in tags:
            session.add(tag)
        session.flush()
        
        # สร้าง Users
        users = [
            User(username="admin", email="admin@painaidee.com", password_hash="hashed_admin_pass", role="admin"),
            User(username="user1", email="user1@example.com", password_hash="hashed_user1_pass", role="user"),
            User(username="user2", email="user2@example.com", password_hash="hashed_user2_pass", role="user"),
        ]
        
        for user in users:
            session.add(user)
        session.flush()
        
        # สร้าง Attractions
        attractions = [
            Attraction(
                name="วัดพระแก้ว",
                description="วัดที่สวยงามและศักดิ์สิทธิ์ในกรุงเทพฯ",
                address="พระนคร กรุงเทพมหานคร",
                province="กรุงเทพมหานคร",
                district="พระนคร",
                latitude=13.7516,
                longitude=100.4921,
                category_id=categories[0].category_id,
                opening_hours="08:30-16:30",
                entrance_fee="500 บาท",
                website="https://www.watphrakaew.com"
            ),
            Attraction(
                name="ตลาดจตุจักร",
                description="ตลาดนัดที่ใหญ่ที่สุดในประเทศไทย",
                address="จตุจักร กรุงเทพมหานคร",
                province="กรุงเทพมหานคร",
                district="จตุจักร",
                latitude=13.7998,
                longitude=100.5493,
                category_id=categories[0].category_id,
                opening_hours="06:00-18:00",
                entrance_fee="ฟรี",
                website="https://www.chatuchakmarket.org"
            ),
            Attraction(
                name="ร้านข้าวแกงดัง",
                description="ร้านอาหารไทยแท้รสชาติดี",
                address="สีลม กรุงเทพมหานคร",
                province="กรุงเทพมหานคร",
                district="บางรัก",
                latitude=13.7250,
                longitude=100.5364,
                category_id=categories[1].category_id,
                opening_hours="10:00-22:00",
                entrance_fee="ไม่มี",
                contact_phone="02-123-4567"
            ),
        ]
        
        for attraction in attractions:
            session.add(attraction)
        session.flush()
        
        # สร้าง Reviews
        reviews = [
            Review(
                attraction_id=attractions[0].id,
                user_id=users[1].user_id,
                rating=5,
                comment="สวยงามมาก แนะนำให้มาเที่ยว",
                created_at=datetime.now() - timedelta(days=5)
            ),
            Review(
                attraction_id=attractions[1].id,
                user_id=users[2].user_id,
                rating=4,
                comment="ของเยอะ แต่คนเยอะด้วย",
                created_at=datetime.now() - timedelta(days=3)
            ),
            Review(
                attraction_id=attractions[2].id,
                user_id=users[1].user_id,
                rating=5,
                comment="อาหารอร่อยมาก ราคาดี",
                created_at=datetime.now() - timedelta(days=1)
            ),
        ]
        
        for review in reviews:
            session.add(review)
        
        # สร้าง Favorites
        favorites = [
            Favorite(user_id=users[1].user_id, attraction_id=attractions[0].id),
            Favorite(user_id=users[1].user_id, attraction_id=attractions[2].id),
            Favorite(user_id=users[2].user_id, attraction_id=attractions[1].id),
        ]
        
        for favorite in favorites:
            session.add(favorite)
        
        # สร้าง AttractionTags
        attraction_tags = [
            AttractionTag(attraction_id=attractions[0].id, tag_id=tags[0].tag_id),  # วัดพระแก้ว - สวยงาม
            AttractionTag(attraction_id=attractions[0].id, tag_id=tags[3].tag_id),  # วัดพระแก้ว - ประวัติศาสตร์
            AttractionTag(attraction_id=attractions[1].id, tag_id=tags[4].tag_id),  # ตลาดจตุจักร - ครอบครัว
            AttractionTag(attraction_id=attractions[2].id, tag_id=tags[2].tag_id),  # ร้านอาหาร - อร่อย
        ]
        
        for attraction_tag in attraction_tags:
            session.add(attraction_tag)
        
        session.commit()
        print("✅ สร้างข้อมูลตัวอย่างสำเร็จ")
        
        # แสดงสถิติ
        print(f"📊 สถิติข้อมูล:")
        print(f"   - หมวดหมู่: {len(categories)} รายการ")
        print(f"   - แท็ก: {len(tags)} รายการ") 
        print(f"   - ผู้ใช้: {len(users)} คน")
        print(f"   - สถานที่: {len(attractions)} แห่ง")
        print(f"   - รีวิว: {len(reviews)} รีวิว")
        print(f"   - รายการโปรด: {len(favorites)} รายการ")
        
        return True
        
    except Exception as e:
        session.rollback()
        print(f"❌ ข้อผิดพลาดในการสร้างข้อมูล: {e}")
        return False
    finally:
        session.close()

def test_database_queries():
    """ทดสอบการ query ข้อมูล"""
    session = SessionLocal()
    try:
        print("\n🔍 ทดสอบการ query ข้อมูล:")
        
        # ทดสอบดึงสถานที่ทั้งหมด
        attractions = session.query(Attraction).all()
        print(f"✅ ดึงสถานที่ท่องเที่ยว: {len(attractions)} แห่ง")
        
        for attraction in attractions:
            print(f"   - {attraction.name} ({attraction.province})")
        
        # ทดสอบดึงรีวิวพร้อมข้อมูลผู้ใช้และสถานที่
        reviews = session.query(Review).join(User).join(Attraction).all()
        print(f"\n✅ ดึงรีวิวพร้อมข้อมูลเจ้าของ: {len(reviews)} รีวิว")
        
        for review in reviews:
            print(f"   - {review.user.username} รีวิว '{review.attraction.name}': {review.rating}⭐ - {review.comment}")
        
        # ทดสอบดึงสถานที่ตามหมวดหมู่
        category = session.query(Category).filter_by(name="สถานที่ท่องเที่ยว").first()
        if category:
            attractions_in_category = session.query(Attraction).filter_by(category_id=category.category_id).all()
            print(f"\n✅ สถานที่ในหมวด '{category.name}': {len(attractions_in_category)} แห่ง")
        
        return True
        
    except Exception as e:
        print(f"❌ ข้อผิดพลาดในการทดสอบ query: {e}")
        return False
    finally:
        session.close()

def main():
    """ฟังก์ชันหลัก"""
    print("🧪 เริ่มทดสอบระบบฐานข้อมูล PaiNaiDee\n")
    
    # 1. สร้างตาราง
    if not create_test_database():
        return
    
    # 2. ลบข้อมูลเก่า
    clear_test_data()
    
    # 3. สร้างข้อมูลทดสอบ
    if not create_sample_data():
        return
    
    # 4. ทดสอบการ query
    if not test_database_queries():
        return
    
    print("\n🎉 การทดสอบเสร็จสิ้น - ระบบฐานข้อมูลทำงานได้ปกติ!")
    print("\n💡 ขั้นตอนถัดไป:")
    print("   1. เริ่มต้น API server: uvicorn api.main:app --reload")
    print("   2. เข้าดู API documentation: http://localhost:8000/docs")
    print("   3. ทดสอบ endpoints: http://localhost:8000/attractions")

if __name__ == "__main__":
    main()