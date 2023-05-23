from sqlalchemy import Column, Integer, String
from database.base import Base

class OperatorEntity(Base):
    __tablename__ = 'operator'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    ranking = Column(Integer, default=0)
