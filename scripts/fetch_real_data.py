import requests
import sys
import os

# Add the parent directory to the path to import from api
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def fetch_tat_data():
    """ดึงข้อมูลจาก Tourism Authority of Thailand API"""
    try:
        # ลองดึงข้อมูลจาก TAT API
        api_url = "https://tatapi.tourismthailand.org/api/tourism/v1/attraction"
        print(f"กำลังดึงข้อมูลจาก: {api_url}")
        
        response = requests.get(api_url, timeout=10)
        
        if response.ok:
            data = response.json()
            print(f"ดึงข้อมูลสำเร็จ: {len(data) if isinstance(data, list) else 'ข้อมูลไม่ใช่ list'} รายการ")
            return data
        else:
            print(f"ไม่สามารถดึงข้อมูลได้: HTTP {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return None
            
    except requests.exceptions.Timeout:
        print("การดึงข้อมูลใช้เวลานานเกินไป (timeout)")
        return None
    except requests.exceptions.ConnectionError:
        print("ไม่สามารถเชื่อมต่อกับ API ได้")
        return None
    except requests.exceptions.RequestException as e:
        print(f"ข้อผิดพลาดในการดึงข้อมูล: {e}")
        return None
    except Exception as e:
        print(f"ข้อผิดพลาดที่ไม่คาดคิด: {e}")
        return None

def fetch_jsonplaceholder_data():
    """ดึงข้อมูลทดสอบจาก JSONPlaceholder"""
    try:
        api_url = "https://jsonplaceholder.typicode.com/posts"
        print(f"กำลังดึงข้อมูลทดสอบจาก: {api_url}")
        
        response = requests.get(api_url, timeout=10)
        
        if response.ok:
            data = response.json()
            print(f"ดึงข้อมูลทดสอบสำเร็จ: {len(data)} รายการ")
            return data
        else:
            print(f"ไม่สามารถดึงข้อมูลทดสอบได้: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"ข้อผิดพลาดในการดึงข้อมูลทดสอบ: {e}")
        return None

if __name__ == "__main__":
    print("=== ทดสอบการดึงข้อมูลจาก API ===")
    
    # ลองดึงข้อมูลจาก TAT API ก่อน
    tat_data = fetch_tat_data()
    
    if not tat_data:
        print("\n=== ไม่สามารถดึงข้อมูลจาก TAT API ได้ ลองใช้ข้อมูลทดสอบ ===")
        test_data = fetch_jsonplaceholder_data()
        
        if test_data:
            print("สามารถใช้ข้อมูลทดสอบได้ - API connection ทำงานปกติ")
        else:
            print("ไม่สามารถดึงข้อมูลได้เลย - ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต")
    else:
        print("สำเร็จ! สามารถดึงข้อมูลจาก TAT API ได้")
