from database.models.locationmodel import DBLocation
from typing import List
from sqlalchemy.sql.expression import desc
from ..models.cyclemodel import DBCycle, Cycle
from sqlalchemy.orm import Session

""""
All database actions associated with the cycle resource
"""
async def get_cycle(db: Session, cycle: int):
    nodes_in_cycle = db.query(DBCycle).filter(DBCycle.cycle == cycle).all()
    for node in nodes_in_cycle:
        node.online_ratio = (node.online_ratio * 100)
        node.version = None if node.version is None else node.version.replace('v', '')
    return nodes_in_cycle

async def get_cycles(db: Session) -> List[DBCycle]:
    return db.query(DBCycle).all()

async def get_distinct_ips_from_cycles(db: Session) -> List[DBCycle]:
    last_cycle = db.query(DBCycle).order_by(desc(DBCycle.cycle)).first().cycle
    active_ips = db.query(DBCycle.ip).filter(DBCycle.cycle == last_cycle).filter(DBCycle.ip.notin_(db.query(DBLocation.ip))).all()
    return active_ips

async def get_last_cycle(db: Session) -> List[DBCycle]:
    return db.query(DBCycle).order_by(desc(DBCycle.cycle)).all()

async def update_current_cycle(db: Session, cycle: Cycle):
    existing_cycle = db.query(DBCycle).filter(DBCycle.cycle == cycle.cycle).filter(DBCycle.ip == cycle.ip).first()
    if existing_cycle is None:
        db_cycle = DBCycle(**cycle.dict())
        db.add(db_cycle)
        db.commit()
        db.refresh(db_cycle)
        return db_cycle
    else:
        existing_cycle.cycle = cycle.cycle
        existing_cycle.ip = cycle.ip
        existing_cycle.address = cycle.address
        existing_cycle.node_name = cycle.node_name
        existing_cycle.online_ratio = cycle.online_ratio
        existing_cycle.created_at = cycle.created_at
        existing_cycle.isAlive = cycle.isAlive
        existing_cycle.version = cycle.version
        existing_cycle.height = cycle.height
        existing_cycle.msg = cycle.msg
        db.add(existing_cycle)
        db.commit()
        db.refresh(existing_cycle)
        return existing_cycle

async def create_cycle(db: Session, dr: Cycle):
    db_cycle = DBCycle(**dr.dict())
    db.add(db_cycle)
    db.commit()
    db.refresh(db_cycle)

    return db_cycle

async def get_node_status_by_cycle(db: Session, cycle: int):
    return db.query(DBCycle).filter(DBCycle.cycle == cycle).all()

async def get_node_status_between_cycles(db: Session, first_cycle: int, last_cycle: int):
    return db.query(DBCycle).filter(DBCycle.cycle >= first_cycle).filter(DBCycle.cycle <= last_cycle).all()

async def get_node_status_by_cycle_for_address(db: Session, cycle: int, vite_address: str):
    return db.query(DBCycle).filter(DBCycle.cycle == cycle).filter(DBCycle.address == vite_address).all()
