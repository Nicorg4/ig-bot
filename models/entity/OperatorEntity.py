from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OperatorEntity(Base):
    __tablename__ = 'operator'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)