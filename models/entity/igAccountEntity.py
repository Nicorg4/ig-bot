from sqlalchemy import Column, Integer, String, ForeignKey
from database.base import Base
from sqlalchemy.orm import relationship
from .OperatorEntity import OperatorEntity

class IgAccountEntity(Base):
    __tablename__ = 'igAccount'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    owner = Column(Integer, ForeignKey('operator.id'))

    owner_obj = relationship(OperatorEntity)