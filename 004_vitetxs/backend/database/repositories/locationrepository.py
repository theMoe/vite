from ..models.locationmodel import DBLocation
from sqlalchemy.orm import Session

""""
All database actions associated with the location resource
"""
async def get_location(db: Session, ip: str) -> DBLocation:
    return db.query(DBLocation).filter(DBLocation.ip == ip).first()


async def create_location(db: Session, dr: DBLocation):
    existing_entry = await get_location(db, dr.ip)
    if existing_entry is None: 
        db.add(dr)
        db.commit()
        db.refresh(dr)
    else:
        existing_entry.city = dr.city
        existing_entry.country = dr.country
        existing_entry.country_code = dr.country_code
        existing_entry.lat = dr.lat
        existing_entry.lon = dr.lon
        existing_entry.org = dr.org
        existing_entry.region = dr.region
        existing_entry.region_name = dr.region_name
        existing_entry.zip = dr.zip
        db.add(existing_entry)
        db.commit()

    return dr
