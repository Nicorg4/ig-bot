from sqlalchemy import Column, Integer, JSON
from database.base import Base

class CycleEntity(Base):
    __tablename__ = 'cycle'
    id = Column(Integer, primary_key=True)
    destinationParamsList = Column(JSON)