# database/init_db.py
from sqlalchemy import create_engine
from .db_session import Base, DATABASE_URL

def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)