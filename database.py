from sqlite3 import IntegrityError
from sqlalchemy import create_engine, Column, String, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
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
        print("No transformed data available for insertion.")
        return

    try:
        for item in transformed_data:
            collection = Collection(**item)
            session.add(collection)
        session.commit()
        print("Data successfully loaded into the database!!!!! :)")

    except IntegrityError as e:
        session.rollback() 
        print(f"Database Integrity Error: {e}")
    
    except Exception as e:
        session.rollback()
        print(f"databUnexpected Database Error: {e}")


def fetch_data(table_name, filters=None, order_by=None, limit=None, like_filters=None, in_filters=None):
    """
    Retrieve data from a table with optional filtering, ordering, and limits.
    """
    if table_name not in Base.metadata.tables:
        print(f"❌ Table '{table_name}' does not exist.")
        return []

    table = Base.metadata.tables[table_name]  
    query = session.query(table)

    query = apply_filters(query, table, filters, like_filters, in_filters)

    if order_by:
        query = query.order_by(table.c[order_by])

    if limit:
        query = query.limit(limit)

    return query.all()



def insert_data(table_name, data):
    """
    Insert single or multiple rows into a table.
    """
    if table_name not in Base.metadata.tables:
        print(f"❌ Table '{table_name}' does not exist.")
        return

    table = Base.metadata.tables[table_name] 

    try:
        if isinstance(data, dict):  
            data = [data]

        with engine.connect() as conn:
            conn.execute(table.insert(), data)
            conn.commit()
        print(f"Data inserted into '{table_name}' successfully!")

    except IntegrityError as e:
        session.rollback()
        print(f"Database Integrity Error: {e}")

    except Exception as e:
        session.rollback()
        print(f"❌ Unexpected Database Error: {e}")

def update_data(table_name, filters, new_values):
    """
    Update records in a table based on filters.
    """
    if table_name not in Base.metadata.tables:
        print(f"Table '{table_name}' does not exist.")
        return

    table = Base.metadata.tables[table_name]  
    query = session.query(table)

    for column, value in filters.items():
        query = query.filter(table.c[column] == value)

    query.update(new_values)
    session.commit()
    print(f"Data updated in '{table_name}' successfully!")


def delete_data(table_name, filters):
    """
    Delete rows from a table based on filters.
    """
    if table_name not in Base.metadata.tables:
        print(f"Table '{table_name}' does not exist.")
        return

    table = Base.metadata.tables[table_name]  
    query = session.query(table)

    for column, value in filters.items():
        query = query.filter(table.c[column] == value)

    deleted_count = query.delete(synchronize_session=False)  
    session.commit()
    print(f"🗑️ Deleted {deleted_count} record(s) from '{table_name}'.")

def apply_filters(query, table, filters=None, like_filters=None, ilike_filters=None, in_filters=None):
    """
    Apply filtering conditions to a SQLAlchemy query.
    Supports:
    - Exact match (`filters`)
    - Partial match (`LIKE`)
    - List match (`IN`)
    """
    if filters:
        for column, value in filters.items():
            query = query.filter(table.c[column] == value)

    if like_filters:
        for column, value in like_filters.items():
            query = query.filter(table.c[column].like(f"%{value}%"))

    if in_filters:
        for column, values in in_filters.items():
            query = query.filter(table.c[column].in_(values))

    return query
