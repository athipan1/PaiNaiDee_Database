import pandas as pd
import json
import csv
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging
from datetime import datetime

# Import models from the main db_script.py to ensure compatibility
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_script import SessionLocal, User, Attraction, Category, Tag, Review, Favorite, Image, AttractionTag

logger = logging.getLogger(__name__)

class DataExporter:
    """Class for exporting data to various formats."""
    
    def __init__(self):
        self.session = SessionLocal()
    
    def __del__(self):
        if hasattr(self, 'session'):
            self.session.close()
    
    def export_to_csv(self, table_name: str, filename: Optional[str] = None) -> str:
        """Export table data to CSV format."""
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{table_name}_{timestamp}.csv"
            
            data = self._get_table_data(table_name)
            if not data:
                raise ValueError(f"No data found for table {table_name}")
            
            df = pd.DataFrame(data)
            
            # Ensure the exports directory exists
            Path("exports").mkdir(exist_ok=True)
            filepath = Path("exports") / filename
            
            df.to_csv(filepath, index=False, encoding='utf-8')
            logger.info(f"Exported {len(data)} records from {table_name} to {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error exporting {table_name} to CSV: {e}")
            raise
    
    def export_to_json(self, table_name: str, filename: Optional[str] = None) -> str:
        """Export table data to JSON format."""
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{table_name}_{timestamp}.json"
            
            data = self._get_table_data(table_name)
            if not data:
                raise ValueError(f"No data found for table {table_name}")
            
            # Ensure the exports directory exists
            Path("exports").mkdir(exist_ok=True)
            filepath = Path("exports") / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            
            logger.info(f"Exported {len(data)} records from {table_name} to {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error exporting {table_name} to JSON: {e}")
            raise
    
    def export_all_tables(self, format_type: str = "json") -> Dict[str, str]:
        """Export all tables to specified format."""
        tables = ["users", "categories", "tags", "attractions", "reviews", "favorites", "images", "attraction_tags"]
        results = {}
        
        for table in tables:
            try:
                if format_type.lower() == "csv":
                    filepath = self.export_to_csv(table)
                elif format_type.lower() == "json":
                    filepath = self.export_to_json(table)
                else:
                    raise ValueError("Format must be 'csv' or 'json'")
                
                results[table] = filepath
            except Exception as e:
                logger.error(f"Failed to export {table}: {e}")
                results[table] = f"Error: {e}"
        
        return results
    
    def _get_table_data(self, table_name: str) -> List[Dict[str, Any]]:
        """Get data from specified table."""
        try:
            if table_name == "users":
                records = self.session.query(User).all()
                return [self._user_to_dict(record) for record in records]
            
            elif table_name == "categories":
                records = self.session.query(Category).all()
                return [self._category_to_dict(record) for record in records]
            
            elif table_name == "tags":
                records = self.session.query(Tag).all()
                return [self._tag_to_dict(record) for record in records]
            
            elif table_name == "attractions":
                records = self.session.query(Attraction).all()
                return [self._attraction_to_dict(record) for record in records]
            
            elif table_name == "reviews":
                records = self.session.query(Review).all()
                return [self._review_to_dict(record) for record in records]
            
            elif table_name == "favorites":
                records = self.session.query(Favorite).all()
                return [self._favorite_to_dict(record) for record in records]
            
            elif table_name == "images":
                records = self.session.query(Image).all()
                return [self._image_to_dict(record) for record in records]
            
            elif table_name == "attraction_tags":
                records = self.session.query(AttractionTag).all()
                return [self._attraction_tag_to_dict(record) for record in records]
            
            else:
                raise ValueError(f"Unknown table name: {table_name}")
        
        except Exception as e:
            logger.error(f"Error getting data from {table_name}: {e}")
            raise
    
    def _user_to_dict(self, user: User) -> Dict[str, Any]:
        """Convert User object to dictionary."""
        return {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "avatar_url": user.avatar_url,
            "role": user.role
            # Note: password_hash is excluded for security
        }
    
    def _category_to_dict(self, category: Category) -> Dict[str, Any]:
        """Convert Category object to dictionary."""
        return {
            "category_id": category.category_id,
            "name": category.name,
            "description": category.description,
            "icon_url": category.icon_url
        }
    
    def _tag_to_dict(self, tag: Tag) -> Dict[str, Any]:
        """Convert Tag object to dictionary."""
        return {
            "tag_id": tag.tag_id,
            "name": tag.name
        }
    
    def _attraction_to_dict(self, attraction: Attraction) -> Dict[str, Any]:
        """Convert Attraction object to dictionary."""
        return {
            "id": attraction.id,
            "name": attraction.name,
            "description": attraction.description,
            "address": attraction.address,
            "province": attraction.province,
            "district": attraction.district,
            "latitude": attraction.latitude,
            "longitude": attraction.longitude,
            "category_id": attraction.category_id,
            "opening_hours": attraction.opening_hours,
            "entrance_fee": attraction.entrance_fee,
            "contact_phone": attraction.contact_phone,
            "website": attraction.website,
            "main_image_url": attraction.main_image_url
        }
    
    def _review_to_dict(self, review: Review) -> Dict[str, Any]:
        """Convert Review object to dictionary."""
        return {
            "id": review.id,
            "attraction_id": review.attraction_id,
            "user_id": review.user_id,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at.isoformat() if review.created_at else None
        }
    
    def _favorite_to_dict(self, favorite: Favorite) -> Dict[str, Any]:
        """Convert Favorite object to dictionary."""
        return {
            "id": favorite.id,
            "user_id": favorite.user_id,
            "attraction_id": favorite.attraction_id
        }
    
    def _image_to_dict(self, image: Image) -> Dict[str, Any]:
        """Convert Image object to dictionary."""
        return {
            "id": image.id,
            "attraction_id": image.attraction_id,
            "image_url": image.image_url,
            "caption": image.caption
        }
    
    def _attraction_tag_to_dict(self, attraction_tag: AttractionTag) -> Dict[str, Any]:
        """Convert AttractionTag object to dictionary."""
        return {
            "attraction_id": attraction_tag.attraction_id,
            "tag_id": attraction_tag.tag_id
        }

class DataImporter:
    """Class for importing data from various formats."""
    
    def __init__(self):
        self.session = SessionLocal()
    
    def __del__(self):
        if hasattr(self, 'session'):
            self.session.close()
    
    def import_from_csv(self, table_name: str, filepath: str, update_existing: bool = False) -> Dict[str, Any]:
        """Import data from CSV file."""
        try:
            df = pd.read_csv(filepath)
            data = df.to_dict('records')
            return self._import_data(table_name, data, update_existing)
        
        except Exception as e:
            logger.error(f"Error importing {table_name} from CSV: {e}")
            raise
    
    def import_from_json(self, table_name: str, filepath: str, update_existing: bool = False) -> Dict[str, Any]:
        """Import data from JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                raise ValueError("JSON data must be a list of objects")
            
            return self._import_data(table_name, data, update_existing)
        
        except Exception as e:
            logger.error(f"Error importing {table_name} from JSON: {e}")
            raise
    
    def _import_data(self, table_name: str, data: List[Dict[str, Any]], update_existing: bool = False) -> Dict[str, Any]:
        """Import data into specified table."""
        results = {
            "total_records": len(data),
            "imported": 0,
            "updated": 0,
            "skipped": 0,
            "errors": []
        }
        
        try:
            for record in data:
                try:
                    if table_name == "users":
                        result = self._import_user(record, update_existing)
                    elif table_name == "categories":
                        result = self._import_category(record, update_existing)
                    elif table_name == "tags":
                        result = self._import_tag(record, update_existing)
                    elif table_name == "attractions":
                        result = self._import_attraction(record, update_existing)
                    elif table_name == "reviews":
                        result = self._import_review(record, update_existing)
                    elif table_name == "favorites":
                        result = self._import_favorite(record, update_existing)
                    elif table_name == "images":
                        result = self._import_image(record, update_existing)
                    elif table_name == "attraction_tags":
                        result = self._import_attraction_tag(record, update_existing)
                    else:
                        raise ValueError(f"Unknown table name: {table_name}")
                    
                    if result == "imported":
                        results["imported"] += 1
                    elif result == "updated":
                        results["updated"] += 1
                    elif result == "skipped":
                        results["skipped"] += 1
                
                except Exception as e:
                    error_msg = f"Error processing record {record}: {e}"
                    logger.error(error_msg)
                    results["errors"].append(error_msg)
            
            self.session.commit()
            logger.info(f"Import completed for {table_name}: {results}")
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Import failed for {table_name}: {e}")
            raise
        
        return results
    
    def _import_user(self, data: Dict[str, Any], update_existing: bool = False) -> str:
        """Import user record."""
        username = data.get("username")
        email = data.get("email")
        
        if not username or not email:
            raise ValueError("Username and email are required")
        
        existing = self.session.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing:
            if update_existing:
                existing.avatar_url = data.get("avatar_url", existing.avatar_url)
                existing.role = data.get("role", existing.role)
                return "updated"
            else:
                return "skipped"
        
        # Create new user (password_hash should be provided or generated)
        user = User(
            username=username,
            email=email,
            password_hash=data.get("password_hash", "changeme"),  # Should be hashed properly
            avatar_url=data.get("avatar_url"),
            role=data.get("role", "user")
        )
        
        self.session.add(user)
        return "imported"
    
    def _import_category(self, data: Dict[str, Any], update_existing: bool = False) -> str:
        """Import category record."""
        name = data.get("name")
        if not name:
            raise ValueError("Category name is required")
        
        existing = self.session.query(Category).filter(Category.name == name).first()
        
        if existing:
            if update_existing:
                existing.description = data.get("description", existing.description)
                existing.icon_url = data.get("icon_url", existing.icon_url)
                return "updated"
            else:
                return "skipped"
        
        category = Category(
            name=name,
            description=data.get("description"),
            icon_url=data.get("icon_url")
        )
        
        self.session.add(category)
        return "imported"
    
    def _import_tag(self, data: Dict[str, Any], update_existing: bool = False) -> str:
        """Import tag record."""
        name = data.get("name")
        if not name:
            raise ValueError("Tag name is required")
        
        existing = self.session.query(Tag).filter(Tag.name == name).first()
        
        if existing:
            return "skipped"  # Tags don't have other fields to update
        
        tag = Tag(name=name)
        self.session.add(tag)
        return "imported"
    
    def _import_attraction(self, data: Dict[str, Any], update_existing: bool = False) -> str:
        """Import attraction record."""
        name = data.get("name")
        if not name:
            raise ValueError("Attraction name is required")
        
        existing = self.session.query(Attraction).filter(Attraction.name == name).first()
        
        if existing:
            if update_existing:
                for field in ["description", "address", "province", "district", "latitude", 
                             "longitude", "category_id", "opening_hours", "entrance_fee", 
                             "contact_phone", "website", "main_image_url"]:
                    if field in data:
                        setattr(existing, field, data[field])
                return "updated"
            else:
                return "skipped"
        
        attraction = Attraction(
            name=name,
            description=data.get("description"),
            address=data.get("address"),
            province=data.get("province"),
            district=data.get("district"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            category_id=data.get("category_id"),
            opening_hours=data.get("opening_hours"),
            entrance_fee=data.get("entrance_fee"),
            contact_phone=data.get("contact_phone"),
            website=data.get("website"),
            main_image_url=data.get("main_image_url")
        )
        
        self.session.add(attraction)
        return "imported"
    
    def _import_review(self, data: Dict[str, Any], update_existing: bool = False) -> str:
        """Import review record."""
        attraction_id = data.get("attraction_id")
        user_id = data.get("user_id")
        rating = data.get("rating")
        
        if not all([attraction_id, user_id, rating]):
            raise ValueError("attraction_id, user_id, and rating are required")
        
        existing = self.session.query(Review).filter(
            Review.attraction_id == attraction_id,
            Review.user_id == user_id
        ).first()
        
        if existing:
            if update_existing:
                existing.rating = rating
                existing.comment = data.get("comment", existing.comment)
                return "updated"
            else:
                return "skipped"
        
        review = Review(
            attraction_id=attraction_id,
            user_id=user_id,
            rating=rating,
            comment=data.get("comment")
        )
        
        self.session.add(review)
        return "imported"
    
    def _import_favorite(self, data: Dict[str, Any], update_existing: bool = False) -> str:
        """Import favorite record."""
        user_id = data.get("user_id")
        attraction_id = data.get("attraction_id")
        
        if not all([user_id, attraction_id]):
            raise ValueError("user_id and attraction_id are required")
        
        existing = self.session.query(Favorite).filter(
            Favorite.user_id == user_id,
            Favorite.attraction_id == attraction_id
        ).first()
        
        if existing:
            return "skipped"  # Favorites are unique by design
        
        favorite = Favorite(
            user_id=user_id,
            attraction_id=attraction_id
        )
        
        self.session.add(favorite)
        return "imported"
    
    def _import_image(self, data: Dict[str, Any], update_existing: bool = False) -> str:
        """Import image record."""
        attraction_id = data.get("attraction_id")
        image_url = data.get("image_url")
        
        if not all([attraction_id, image_url]):
            raise ValueError("attraction_id and image_url are required")
        
        existing = self.session.query(Image).filter(
            Image.attraction_id == attraction_id,
            Image.image_url == image_url
        ).first()
        
        if existing:
            if update_existing:
                existing.caption = data.get("caption", existing.caption)
                return "updated"
            else:
                return "skipped"
        
        image = Image(
            attraction_id=attraction_id,
            image_url=image_url,
            caption=data.get("caption")
        )
        
        self.session.add(image)
        return "imported"
    
    def _import_attraction_tag(self, data: Dict[str, Any], update_existing: bool = False) -> str:
        """Import attraction_tag record."""
        attraction_id = data.get("attraction_id")
        tag_id = data.get("tag_id")
        
        if not all([attraction_id, tag_id]):
            raise ValueError("attraction_id and tag_id are required")
        
        existing = self.session.query(AttractionTag).filter(
            AttractionTag.attraction_id == attraction_id,
            AttractionTag.tag_id == tag_id
        ).first()
        
        if existing:
            return "skipped"  # AttractionTags are unique by design
        
        attraction_tag = AttractionTag(
            attraction_id=attraction_id,
            tag_id=tag_id
        )
        
        self.session.add(attraction_tag)
        return "imported"

# Convenience functions
def export_users_csv(filename: str = None) -> str:
    """Export users to CSV."""
    exporter = DataExporter()
    return exporter.export_to_csv("users", filename)

def export_attractions_csv(filename: str = None) -> str:
    """Export attractions to CSV."""
    exporter = DataExporter()
    return exporter.export_to_csv("attractions", filename)

def export_all_data(format_type: str = "json") -> Dict[str, str]:
    """Export all data to specified format."""
    exporter = DataExporter()
    return exporter.export_all_tables(format_type)

def import_users_csv(filepath: str, update_existing: bool = False) -> Dict[str, Any]:
    """Import users from CSV."""
    importer = DataImporter()
    return importer.import_from_csv("users", filepath, update_existing)

def import_attractions_csv(filepath: str, update_existing: bool = False) -> Dict[str, Any]:
    """Import attractions from CSV."""
    importer = DataImporter()
    return importer.import_from_csv("attractions", filepath, update_existing)

# Example usage and testing
if __name__ == "__main__":
    # Example exports
    print("Exporting data...")
    try:
        results = export_all_data("json")
        for table, filepath in results.items():
            print(f"{table}: {filepath}")
    except Exception as e:
        print(f"Export failed: {e}")
    
    # Example import (commented out to avoid accidental execution)
    # print("Importing data...")
    # try:
    #     result = import_users_csv("exports/users.csv")
    #     print(f"Import result: {result}")
    # except Exception as e:
    #     print(f"Import failed: {e}")
