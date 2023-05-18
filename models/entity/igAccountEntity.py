from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class IgAccountEntity(Base):
    __tablename__ = 'igAccount'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    owner = Column(Integer, ForeignKey('operator.id'))
    owner = relationship("Operator")