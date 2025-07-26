import pandas as pd
import sys
import os

# Add the parent directory to the path to import from api
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.deps import SessionLocal
from api.models import User, Attraction

def export_users_csv(filename="users.csv"):
    session = SessionLocal()
    try:
        users = session.query(User).all()
        # Convert to dict manually to avoid SQLAlchemy internal attributes
        user_data = []
        for user in users:
            user_data.append({
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'password_hash': user.password_hash,
                'avatar_url': user.avatar_url,
                'role': user.role
            })
        df = pd.DataFrame(user_data)
        df.to_csv(filename, index=False)
        print(f"Exported {len(user_data)} users to {filename}")
    except Exception as e:
        print(f"Error exporting users: {e}")
    finally:
        session.close()

def import_users_csv(filename="users.csv"):
    session = SessionLocal()
    try:
        df = pd.read_csv(filename)
        imported_count = 0
        for _, row in df.iterrows():
            # Check if user already exists
            existing_user = session.query(User).filter(
                (User.username == row['username']) | (User.email == row['email'])
            ).first()
            
            if not existing_user:
                user = User(
                    username=row['username'],
                    email=row['email'],
                    password_hash=row['password_hash'],
                    avatar_url=row.get('avatar_url'),
                    role=row.get('role', 'user')
                )
                session.add(user)
                imported_count += 1
        
        session.commit()
        print(f"Imported {imported_count} new users from {filename}")
    except Exception as e:
        session.rollback()
        print(f"Error importing users: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    print("Testing import/export functionality...")
    # This is a test when script is run directly
    export_users_csv("test_users.csv")
