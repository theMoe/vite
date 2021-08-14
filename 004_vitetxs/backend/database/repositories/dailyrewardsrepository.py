from typing import List
from sqlalchemy.sql.expression import desc
from ..models.dailyrewardmodel import DBDailyFullNodeReward, DailyFullNodeRewardOut
from sqlalchemy.orm import Session

""""
All database actions associated with the daily reward resource
"""
async def get_dailyreward(db: Session, dailyreward_id: int):
    return db.query(DBDailyFullNodeReward).where(DBDailyFullNodeReward.id == dailyreward_id).first()

async def get_dailyrewards(db: Session) -> List[DailyFullNodeRewardOut]:
    return db.query(DBDailyFullNodeReward).all()

async def get_limited_dailyrewards(db: Session, limit: int) -> List[DailyFullNodeRewardOut]:
    return db.query(DBDailyFullNodeReward).order_by(desc(DBDailyFullNodeReward.created_at)).limit(limit).all()

async def get_dailyreward_by_block_height(db: Session, block_height: int) -> List[DailyFullNodeRewardOut]:
    return db.query(DBDailyFullNodeReward).filter(DBDailyFullNodeReward.block_height == block_height).all()

async def get_dailyreward_by_cycles(db: Session, cycles: List[int]) -> List[DailyFullNodeRewardOut]:
    return db.query(DBDailyFullNodeReward).filter(DBDailyFullNodeReward.cycle.in_(cycles)).all()

async def create_dailyreward(db: Session, dr: DBDailyFullNodeReward):
    db.add(dr)
    db.commit()
    db.refresh(dr)

    return dr