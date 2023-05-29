from sqlalchemy import Column, Integer, String
from database.base import Base

class DestinationEntity(Base):
    __tablename__ = 'destination'
    id = Column(Integer, primary_key=True)
    locationId = Column(String)
    locationName = Column(String)
    placeName = Column(String)
    hashtag = Column(String)
    type = Column(String)