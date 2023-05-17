from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DestinationEntity(Base):
    __tablename__ = 'destination'
    id = Column(Integer, primary_key=True)
    locationId = Column(String)
    locationName = Column(String)
    placeName = Column(String)
    hashtag = Column(String)