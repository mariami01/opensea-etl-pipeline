from sqlite3 import IntegrityError
from sqlalchemy import create_engine, Column, String, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

os.makedirs("data", exist_ok=True)
DATABASE_URL = "sqlite:///data/opensea_collections.db"

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    collection = Column(String, unique=True)
    name = Column(String)
    description = Column(String)
    image_url = Column(String)
    owner = Column(String)
    twitter_username = Column(String)
    contracts = Column(JSON)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def load_data_to_db(transformed_data):
    """
    Loads transformed data into the database with error handling.
    """
    if not transformed_data:
        print("❌ No transformed data available for insertion.")
        return

    try:
        for item in transformed_data:
            collection = Collection(**item)
            session.add(collection)
        session.commit()
        print("✅ Data successfully loaded into the database.")

    except IntegrityError as e:
        session.rollback() 
        print(f"❌ Database Integrity Error: {e}")
    
    except Exception as e:
        session.rollback()
        print(f"❌ Unexpected Database Error: {e}")