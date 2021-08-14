from typing import Optional
from database.models.locationmodel import DBLocation
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, Float
from sqlalchemy.types import DateTime
from datetime import datetime
from database.models import Base


class DBCycle(Base):
    __tablename__ = "Cycles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cycle = Column(Integer, index=True) 
    ip = Column(String(15), nullable=False)
    created_at = Column(DateTime)
    address = Column(String(255), index=True)
    node_name = Column(String(255))
    online_ratio = Column(Float)
    isAlive = Column(Boolean)
    version = Column(String(50))
    height = Column(Integer)
    msg = Column(String(255))
    location = relationship('DBLocation', backref='DBCycle',
        primaryjoin='DBLocation.ip==DBCycle.ip', foreign_keys='DBLocation.ip')



class Cycle(BaseModel):
    cycle: int
    created_at: datetime
    ip: str
    address: str
    node_name: str
    online_ratio: float
    isAlive: Optional[bool]
    version: Optional[str]
    height: Optional[int]
    msg: Optional[str]

    class Config:
        orm_mode = True
