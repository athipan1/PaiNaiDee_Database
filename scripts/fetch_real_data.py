import requests
import logging
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import os
from pathlib import Path

# Import database models
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_script import SessionLocal, User, Attraction, Category, Tag, AttractionTag
from scripts.import_export import DataImporter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealDataFetcher:
    """Class for fetching real data from various external sources."""
    
    def __init__(self):
        self.session = SessionLocal()
        self.importer = DataImporter()
        
        # API configurations
        self.tat_api_base = "https://tatapi.tourismthailand.org/api/v1"
        self.headers = {
            'User-Agent': 'PaiNaiDee-App/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        # Rate limiting
        self.request_delay = 1  # seconds between requests
        self.max_retries = 3
    
    def __del__(self):
        if hasattr(self, 'session'):
            self.session.close()
    
    def fetch_tat_attractions(self, province: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch tourist attractions from Tourism Authority of Thailand (TAT) API.
        
        Args:
            province: Optional province name to filter results
            limit: Maximum number of attractions to fetch
            
        Returns:
            List of attraction dictionaries
        """
        logger.info(f"Fetching TAT attractions data (province: {province}, limit: {limit})")
        
        try:
            # TAT API endpoint for attractions
            url = f"{self.tat_api_base}/attraction"
            params = {
                'limit': min(limit, 100),  # TAT API typically limits to 100 per request
                'page': 1
            }
            
            if province:
                params['province'] = province
            
            attractions = []
            page = 1
            
            while len(attractions) < limit:
                params['page'] = page
                
                response = self._make_request(url, params)
                if not response:
                    break
                
                data = response.json()
                
                # Handle different API response structures
                items = []
                if isinstance(data, dict):
                    items = data.get('data', data.get('results', data.get('attractions', [])))
                elif isinstance(data, list):
                    items = data
                
                if not items:
                    logger.info(f"No more data available at page {page}")
                    break
                
                for item in items:
                    if len(attractions) >= limit:
                        break
                    
                    processed_attraction = self._process_tat_attraction(item)
                    if processed_attraction:
                        attractions.append(processed_attraction)
                
                page += 1
                time.sleep(self.request_delay)  # Rate limiting
            
            logger.info(f"Successfully fetched {len(attractions)} attractions from TAT API")
            return attractions
            
        except Exception as e:
            logger.error(f"Error fetching TAT attractions: {e}")
            return []
    
    def fetch_sample_data(self, count: int = 50) -> List[Dict[str, Any]]:
        """
        Fetch sample attraction data from JSONPlaceholder or similar free APIs.
        This serves as a fallback when real tourism APIs are not available.
        """
        logger.info(f"Fetching sample data ({count} items)")
        
        try:
            # Use JSONPlaceholder for sample data
            posts_url = "https://jsonplaceholder.typicode.com/posts"
            users_url = "https://jsonplaceholder.typicode.com/users"
            
            posts_response = self._make_request(posts_url)
            users_response = self._make_request(users_url)
            
            if not posts_response or not users_response:
                return self._generate_mock_data(count)
            
            posts = posts_response.json()[:count]
            users = users_response.json()
            
            # Sample Thai provinces and districts
            provinces = [
                "กรุงเทพมหานคร", "เชียงใหม่", "ภูเก็ต", "ชลบุรี", "กาญจนบุรี", 
                "อยุธยา", "นครราชสีมา", "ขอนแก่น", "อุดรธานี", "สงขลา"
            ]
            
            districts = [
                "เมือง", "บางรัก", "จตุจักร", "ห้วยขวาง", "วัฒนา", 
                "คลองเตย", "ราชเทวี", "ปทุมวัน", "บางกอกน้อย", "บางซื่อ"
            ]
            
            categories = [
                "วัด/สถานที่ศักดิ์สิทธิ์", "พิพิธภัณฑ์", "สวนสาธารณะ", 
                "ตลาด", "ชายหาด", "น้ำตก", "อุทยานแห่งชาติ", "โบราณสถาน"
            ]
            
            attractions = []
            for i, post in enumerate(posts):
                attraction = {
                    "name": post["title"].title(),
                    "description": post["body"],
                    "address": f"{i+1} ถนน {['สุขุมวิท', 'สีลม', 'รัชดา', 'พหลโยธิน'][i % 4]}",
                    "province": provinces[i % len(provinces)],
                    "district": districts[i % len(districts)],
                    "latitude": round(13.7563 + (i * 0.01), 6),  # Around Bangkok
                    "longitude": round(100.5018 + (i * 0.01), 6),
                    "category_name": categories[i % len(categories)],
                    "opening_hours": ["เปิด 24 ชั่วโมง", "จ-ศ 9:00-17:00", "ทุกวัน 8:00-18:00"][i % 3],
                    "entrance_fee": ["ฟรี", "20 บาท", "50 บาท", "100 บาท"][i % 4],
                    "contact_phone": f"+66-{80 + (i % 10)}-{1000000 + i}",
                    "website": f"https://www.example.com/attraction/{post['id']}",
                    "main_image_url": f"https://picsum.photos/seed/{post['id']}/800/600"
                }
                attractions.append(attraction)
            
            logger.info(f"Generated {len(attractions)} sample attractions")
            return attractions
            
        except Exception as e:
            logger.error(f"Error fetching sample data: {e}")
            return self._generate_mock_data(count)
    
    def fetch_thai_provinces(self) -> List[str]:
        """Fetch list of Thai provinces from external API or return predefined list."""
        try:
            # Try to fetch from Thai government API or similar
            # For now, return a comprehensive list of Thai provinces
            provinces = [
                "กรุงเทพมหานคร", "กระบี่", "กาญจนบุรี", "กาฬสินธุ์", "กำแพงเพชร",
                "ขอนแก่น", "จันทบุรี", "ฉะเชิงเทรา", "ชลบุรี", "ชัยนาท",
                "ชัยภูมิ", "ชุมพร", "เชียงราย", "เชียงใหม่", "ตรัง",
                "ตราด", "ตาก", "นครนายก", "นครปฐม", "นครพนม",
                "นครราชสีมา", "นครศรีธรรมราช", "นครสวรรค์", "นนทบุรี", "นราธิวาส",
                "น่าน", "บึงกาฬ", "บุรีรัมย์", "ปทุมธานี", "ประจวบคีรีขันธ์",
                "ปราจีนบุรี", "ปัตตานี", "พระนครศรีอยุธยา", "พะเยา", "พังงา",
                "พัทลุง", "พิจิตร", "พิษณุโลก", "เพชรบุรี", "เพชรบูรณ์",
                "แพร่", "ภูเก็ต", "มหาสารคาม", "มุกดาหาร", "แม่ฮ่องสอน",
                "ยโสธร", "ยะลา", "ร้อยเอ็ด", "ระนอง", "ระยอง",
                "ราชบุรี", "ลพบุรี", "ลำปาง", "ลำพูน", "เลย",
                "ศรีสะเกษ", "สกลนคร", "สงขลา", "สตูล", "สมุทรปราการ",
                "สมุทรสงคราม", "สมุทรสาคร", "สระแก้ว", "สระบุรี", "สิงห์บุรี",
                "สุโขทัย", "สุพรรณบุรี", "สุราษฎร์ธานี", "สุรินทร์", "หนองคาย",
                "หนองบัวลำภู", "อ่างทอง", "อำนาจเจริญ", "อุดรธานี", "อุตรดิตถ์",
                "อุทัยธานี", "อุบลราชธานี"
            ]
            
            logger.info(f"Retrieved {len(provinces)} Thai provinces")
            return provinces
            
        except Exception as e:
            logger.error(f"Error fetching provinces: {e}")
            return []
    
    def save_attractions_to_db(self, attractions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Save fetched attraction data to database."""
        logger.info(f"Saving {len(attractions)} attractions to database")
        
        try:
            # Ensure categories exist
            self._ensure_categories_exist(attractions)
            
            # Transform attraction data to match database schema
            transformed_data = []
            for attraction in attractions:
                # Get or create category
                category_name = attraction.get("category_name", "อื่นๆ")
                category = self.session.query(Category).filter(Category.name == category_name).first()
                
                if not category:
                    category = Category(
                        name=category_name,
                        description=f"หมวดหมู่ {category_name}",
                        icon_url=f"https://example.com/icons/{category_name.lower()}.png"
                    )
                    self.session.add(category)
                    self.session.flush()
                
                # Transform attraction data
                transformed = {
                    "name": attraction.get("name", "ไม่ระบุชื่อ"),
                    "description": attraction.get("description"),
                    "address": attraction.get("address"),
                    "province": attraction.get("province"),
                    "district": attraction.get("district"),
                    "latitude": attraction.get("latitude"),
                    "longitude": attraction.get("longitude"),
                    "category_id": category.category_id,
                    "opening_hours": attraction.get("opening_hours"),
                    "entrance_fee": attraction.get("entrance_fee"),
                    "contact_phone": attraction.get("contact_phone"),
                    "website": attraction.get("website"),
                    "main_image_url": attraction.get("main_image_url")
                }
                
                transformed_data.append(transformed)
            
            # Use the importer to save data
            results = self.importer._import_data("attractions", transformed_data, update_existing=True)
            
            logger.info(f"Saved attractions to database: {results}")
            return results
            
        except Exception as e:
            logger.error(f"Error saving attractions to database: {e}")
            self.session.rollback()
            raise
    
    def _make_request(self, url: str, params: Optional[Dict] = None) -> Optional[requests.Response]:
        """Make HTTP request with retries and error handling."""
        for attempt in range(self.max_retries):
            try:
                response = requests.get(
                    url, 
                    params=params, 
                    headers=self.headers,
                    timeout=30
                )
                response.raise_for_status()
                return response
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"All {self.max_retries} request attempts failed for {url}")
        
        return None
    
    def _process_tat_attraction(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process TAT API attraction data into our format."""
        try:
            # Map TAT API fields to our schema
            # Note: Actual TAT API structure may vary
            processed = {
                "name": item.get("name", item.get("title", "ไม่ระบุชื่อ")),
                "description": item.get("description", item.get("detail", "")),
                "address": item.get("address", ""),
                "province": item.get("province", item.get("province_name", "")),
                "district": item.get("district", item.get("district_name", "")),
                "latitude": float(item.get("latitude", 0)) if item.get("latitude") else None,
                "longitude": float(item.get("longitude", 0)) if item.get("longitude") else None,
                "category_name": item.get("category", item.get("type", "สถานที่ท่องเที่ยว")),
                "opening_hours": item.get("opening_hours", item.get("open_time", "")),
                "entrance_fee": item.get("entrance_fee", item.get("fee", "")),
                "contact_phone": item.get("phone", item.get("contact", "")),
                "website": item.get("website", item.get("url", "")),
                "main_image_url": item.get("image", item.get("photo", ""))
            }
            
            # Validate required fields
            if not processed["name"] or processed["name"] == "ไม่ระบุชื่อ":
                return None
            
            return processed
            
        except Exception as e:
            logger.error(f"Error processing TAT attraction: {e}")
            return None
    
    def _generate_mock_data(self, count: int) -> List[Dict[str, Any]]:
        """Generate mock attraction data as fallback."""
        logger.info(f"Generating {count} mock attractions")
        
        mock_data = []
        for i in range(count):
            attraction = {
                "name": f"สถานที่ท่องเที่ยว {i+1}",
                "description": f"คำอธิบายสำหรับสถานที่ท่องเที่ยว {i+1}",
                "address": f"{i+1} ถนนตัวอย่าง",
                "province": "กรุงเทพมหานคร",
                "district": "เมือง",
                "latitude": 13.7563 + (i * 0.001),
                "longitude": 100.5018 + (i * 0.001),
                "category_name": "สถานที่ท่องเที่ยว",
                "opening_hours": "ทุกวัน 8:00-18:00",
                "entrance_fee": "ฟรี",
                "contact_phone": f"+66-2-{1000000 + i}",
                "website": f"https://example.com/{i+1}",
                "main_image_url": f"https://picsum.photos/seed/{i}/800/600"
            }
            mock_data.append(attraction)
        
        return mock_data
    
    def _ensure_categories_exist(self, attractions: List[Dict[str, Any]]):
        """Ensure all categories mentioned in attractions exist in database."""
        category_names = set()
        for attraction in attractions:
            category_name = attraction.get("category_name")
            if category_name:
                category_names.add(category_name)
        
        for category_name in category_names:
            existing = self.session.query(Category).filter(Category.name == category_name).first()
            if not existing:
                category = Category(
                    name=category_name,
                    description=f"หมวดหมู่ {category_name}",
                    icon_url=f"https://example.com/icons/{category_name.lower().replace(' ', '_')}.png"
                )
                self.session.add(category)
        
        self.session.commit()

# Convenience functions
def fetch_tat_data(province: Optional[str] = None, limit: int = 50) -> Dict[str, Any]:
    """Fetch data from TAT API and save to database."""
    fetcher = RealDataFetcher()
    
    try:
        # Try TAT API first
        attractions = fetcher.fetch_tat_attractions(province, limit)
        
        # If TAT API fails, use sample data
        if not attractions:
            logger.info("TAT API unavailable, using sample data")
            attractions = fetcher.fetch_sample_data(limit)
        
        if attractions:
            results = fetcher.save_attractions_to_db(attractions)
            return {
                "status": "success",
                "fetched_count": len(attractions),
                "save_results": results
            }
        else:
            return {
                "status": "failed",
                "message": "No data could be fetched"
            }
    
    except Exception as e:
        logger.error(f"Error in fetch_tat_data: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

def fetch_sample_data_to_db(count: int = 30) -> Dict[str, Any]:
    """Fetch sample data and save to database."""
    fetcher = RealDataFetcher()
    
    try:
        attractions = fetcher.fetch_sample_data(count)
        if attractions:
            results = fetcher.save_attractions_to_db(attractions)
            return {
                "status": "success",
                "fetched_count": len(attractions),
                "save_results": results
            }
        else:
            return {
                "status": "failed",
                "message": "No sample data could be generated"
            }
    
    except Exception as e:
        logger.error(f"Error in fetch_sample_data_to_db: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

# Example usage and testing
if __name__ == "__main__":
    print("Testing data fetching...")
    
    # Test sample data fetching
    result = fetch_sample_data_to_db(20)
    print(f"Sample data fetch result: {result}")
    
    # Test TAT data fetching (will fallback to sample data if TAT API is unavailable)
    # result = fetch_tat_data("กรุงเทพมหานคร", 10)
    # print(f"TAT data fetch result: {result}")
