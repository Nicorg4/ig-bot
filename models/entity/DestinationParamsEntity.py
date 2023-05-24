from sqlalchemy import Column, Integer, String, ForeignKey
from database.base import Base
from sqlalchemy.orm import relationship
from .DestinationEntity import DestinationEntity

class DestinationParamsEntity(Base):
    __tablename__ = 'destinationParams'
    id = Column(Integer, primary_key=True)
    destinationId = Column(Integer, ForeignKey('destination.id'))
    numberOfComments = Column(Integer)
    numberOfMessages = Column(Integer)

    destinationId_obj = relationship(DestinationEntity)