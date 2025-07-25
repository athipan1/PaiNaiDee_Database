#!/usr/bin/env python3
"""
PaiNaiDee Database Startup Script
เริ่ม - ไฟล์สำหรับเริ่มต้นการใช้งานระบบฐานข้อมูล PaiNaiDee

This script initializes and starts the PaiNaiDee database system.
It provides options for database setup and API server startup.
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """ตรวจสอบการติดตั้ง dependencies ที่จำเป็น"""
    print("🔍 ตรวจสอบ dependencies...")
    
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import psycopg2
        import pandas
        import httpx
        print("✅ Dependencies ครบถ้วน")
        return True
    except ImportError as e:
        print(f"❌ ขาด dependency: {e}")
        print("📦 กำลังติดตั้ง dependencies...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ ติดตั้ง dependencies สำเร็จ")
            return True
        except subprocess.CalledProcessError:
            print("❌ ไม่สามารถติดตั้ง dependencies ได้")
            return False

def setup_environment():
    """ตั้งค่าตัวแปรสภาพแวดล้อม"""
    print("🌱 ตั้งค่าสภาพแวดล้อม...")
    
    # ตั้งค่า DATABASE_URL ถ้ายังไม่มี
    if not os.getenv("DATABASE_URL"):
        # ใช้ SQLite เป็นค่าเริ่มต้นสำหรับการพัฒนา
        os.environ["DATABASE_URL"] = "sqlite:///./painaidee.db"
        print("📁 ใช้ SQLite database สำหรับการพัฒนา")
    
    print("✅ ตั้งค่าสภาพแวดล้อมสำเร็จ")

def setup_database():
    """สร้างและเตรียมฐานข้อมูล"""
    print("🗄️  กำลังเตรียมฐานข้อมูล...")
    
    try:
        # Import และสร้างตาราง
        from api.models import Base
        from api.deps import engine
        
        # สร้างตารางทั้งหมด
        Base.metadata.create_all(bind=engine)
        print("✅ สร้างตารางฐานข้อมูลสำเร็จ")
        
        return True
    except Exception as e:
        print(f"❌ ไม่สามารถสร้างฐานข้อมูลได้: {e}")
        return False

def populate_sample_data():
    """เพิ่มข้อมูลตัวอย่างลงในฐานข้อมูล"""
    print("📊 กำลังเพิ่มข้อมูลตัวอย่าง...")
    
    try:
        from api.models import User, Category, Tag, Attraction, Base
        from api.deps import SessionLocal
        import hashlib
        
        db = SessionLocal()
        
        # ตรวจสอบว่ามีข้อมูลอยู่แล้วหรือไม่
        if db.query(User).count() > 0:
            print("ℹ️  มีข้อมูลอยู่ในฐานข้อมูลแล้ว")
            db.close()
            return True
        
        # เพิ่มหมวดหมู่ตัวอย่าง
        categories = [
            Category(name="สถานที่ท่องเที่ยว", description="สถานที่ท่องเที่ยวทั่วไป"),
            Category(name="ร้านอาหาร", description="ร้านอาหารและเครื่องดื่ม"),
            Category(name="ที่พัก", description="โรงแรมและที่พัก"),
            Category(name="แหล่งช้อปปิ้ง", description="ตลาดและห้างสรรพสินค้า"),
        ]
        for cat in categories:
            db.add(cat)
        
        # เพิ่มแท็กตัวอย่าง
        tags = [
            Tag(name="สวยงาม"),
            Tag(name="น่าสนใจ"),
            Tag(name="ถ่ายรูปสวย"),
            Tag(name="ครอบครัว"),
        ]
        for tag in tags:
            db.add(tag)
        
        # เพิ่มผู้ใช้ตัวอย่าง
        password_hash = hashlib.sha256("password123".encode()).hexdigest()
        user = User(
            username="demo_user",
            email="demo@painaidee.com",
            password_hash=password_hash,
            role="user"
        )
        db.add(user)
        
        # Commit การเปลี่ยนแปลง
        db.commit()
        
        # เพิ่มสถานที่ตัวอย่าง
        attraction = Attraction(
            name="วัดพระแก้ว",
            description="วัดที่สวยงามในกรุงเทพฯ",
            address="พระนคร กรุงเทพมหานคร",
            province="กรุงเทพมหานคร",
            district="พระนคร",
            latitude=13.751839,
            longitude=100.492417,
            category_id=1,
            opening_hours="08:30-15:30",
            entrance_fee="500 บาท",
            website="https://www.watphrakaew.com"
        )
        db.add(attraction)
        db.commit()
        
        db.close()
        print("✅ เพิ่มข้อมูลตัวอย่างสำเร็จ")
        return True
        
    except Exception as e:
        print(f"❌ ไม่สามารถเพิ่มข้อมูลตัวอย่างได้: {e}")
        return False

def start_api_server(host="127.0.0.1", port=8000, reload=True):
    """เริ่มต้น API server"""
    print(f"🚀 เริ่มต้น API server ที่ http://{host}:{port}")
    print("📖 API Documentation: http://127.0.0.1:8000/docs")
    print("🔄 กด Ctrl+C เพื่อหยุดเซิร์ฟเวอร์")
    
    try:
        # รัน uvicorn จาก root directory โดยใช้ api.main:app
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "api.main:app", 
            "--host", host, 
            "--port", str(port)
        ]
        
        if reload:
            cmd.append("--reload")
            
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 หยุดเซิร์ฟเวอร์แล้ว")
    except Exception as e:
        print(f"❌ ไม่สามารถเริ่มเซิร์ฟเวอร์ได้: {e}")

def run_tests():
    """รันการทดสอบ"""
    print("🧪 กำลังรันการทดสอบ...")
    
    try:
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
            
        if result.returncode == 0:
            print("✅ การทดสอบผ่านทั้งหมด")
        else:
            print("⚠️  การทดสอบมีปัญหา")
            
        return result.returncode == 0
    except Exception as e:
        print(f"❌ ไม่สามารถรันการทดสอบได้: {e}")
        return False

def main():
    """ฟังก์ชันหลักสำหรับเริ่มต้นระบบ"""
    parser = argparse.ArgumentParser(
        description="PaiNaiDee Database Startup Script - เริ่มต้นระบบฐานข้อมูล PaiNaiDee",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
ตัวอย่างการใช้งาน:
  python start.py                    # เริ่มต้นทั้งหมดและรัน API server
  python start.py --init-only        # เตรียมระบบเท่านั้น ไม่รัน server
  python start.py --test             # รันการทดสอบ
  python start.py --host 0.0.0.0     # รัน server ให้เข้าถึงได้จากภายนอก
        """
    )
    
    parser.add_argument("--init-only", action="store_true", 
                       help="เตรียมระบบเท่านั้น ไม่รัน API server")
    parser.add_argument("--test", action="store_true", 
                       help="รันการทดสอบแทนการเริ่ม server")
    parser.add_argument("--host", default="127.0.0.1", 
                       help="Host สำหรับ API server (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, 
                       help="Port สำหรับ API server (default: 8000)")
    parser.add_argument("--no-reload", action="store_true", 
                       help="ปิดการ auto-reload")
    parser.add_argument("--skip-sample-data", action="store_true", 
                       help="ข้ามการเพิ่มข้อมูลตัวอย่าง")
    
    args = parser.parse_args()
    
    print("🌟 ยินดีต้อนรับสู่ PaiNaiDee Database System")
    print("=" * 50)
    
    # ตรวจสอบและติดตั้ง dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # ตั้งค่าสภาพแวดล้อม
    setup_environment()
    
    # ตั้งค่าฐานข้อมูล
    if not setup_database():
        sys.exit(1)
    
    # เพิ่มข้อมูลตัวอย่าง (ถ้าไม่ได้ข้าม)
    if not args.skip_sample_data:
        populate_sample_data()
    
    print("=" * 50)
    
    # รันการทดสอบถ้าระบุ
    if args.test:
        success = run_tests()
        sys.exit(0 if success else 1)
    
    # ถ้าเป็น init-only ให้หยุดที่นี่
    if args.init_only:
        print("✅ เตรียมระบบเสร็จสิ้น")
        print("🚀 ใช้คำสั่ง: python start.py เพื่อเริ่ม API server")
        return
    
    # เริ่ม API server
    start_api_server(
        host=args.host, 
        port=args.port, 
        reload=not args.no_reload
    )

if __name__ == "__main__":
    main()