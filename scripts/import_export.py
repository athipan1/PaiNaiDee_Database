import pandas as pd
from db_script import SessionLocal, User, Attraction

def export_users_csv(filename="users.csv"):
    session = SessionLocal()
    users = session.query(User).all()
    df = pd.DataFrame([u.__dict__ for u in users])
    df.to_csv(filename, index=False)

def import_users_csv(filename="users.csv"):
    session = SessionLocal()
    df = pd.read_csv(filename)
    for _, row in df.iterrows():
        user = User(**row.to_dict())
        session.add(user)
    session.commit()
