from sqlalchemy.sql.sqltypes import Float
from database.models import Base
from pydantic import BaseModel
from sqlalchemy import Column, String


class DBLocation(Base):
    __tablename__ = "Locations"
    
    ip = Column(String(15), primary_key=True, index=True)
    country = Column(String(255))
    country_code = Column(String(10))
    region = Column(String(50))
    region_name = Column(String(255))
    city = Column(String(255))
    zip = Column(String(255))
    lat = Column(Float)
    lon = Column(Float)
    org = Column(String(255))

class LocationIn(BaseModel):
    country: str
    countryCode: str
    region: str
    regionName: str
    city: str
    zip: int
    lat: float
    lon: float
    org: str
    query: str

    class Config:
       orm_mode = True

