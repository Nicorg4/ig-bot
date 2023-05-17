from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class IgAccountEntity(Base):
    __tablename__ = 'igAccount'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    owner = Column(String)