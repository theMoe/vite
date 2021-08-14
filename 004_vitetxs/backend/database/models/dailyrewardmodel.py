from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.sql.sqltypes import Numeric
from sqlalchemy.types import DateTime
from datetime import datetime
from database.models import Base


class DBDailyFullNodeReward(Base):
    __tablename__ = "DailyFullNodeRewards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, index=True)
    symbol = Column(String(255))
    token_id = Column(String(255))
    tweet_id = Column(String(255))
    tx_hash = Column(String(255)) 
    snapshot_hash = Column(String(255))
    amount = Column(Numeric(asdecimal=False))
    amount_normalised = Column(Float)
    token_in_usdt = Column(Float)
    transaction_in_usdt = Column(Float)
    block_height = Column(Integer, index=True)
    decimals = Column(Integer)
    from_address = Column(String(255))
    data = Column(String(255))
    cycle = Column(Integer)

class DailyFullNodeRewardOut(BaseModel):
    symbol: str
    token_id: str
    tweet_id: str
    tx_hash: str
    snapshot_hash: str
    amount: int
    amount_normalised: float
    token_in_usdt: float
    transaction_in_usdt: float
    block_height: int
    decimals: int
    from_address: str
    created_at: datetime
    data: Optional[str]
    cycle: Optional[int]
    class Config:
        orm_mode = True

class DailyFullNodeRewardIn(BaseModel):
    symbol: str
    token_id: str
    tweet_id: str
    tx_hash: str
    snapshot_hash: str
    amount: int
    token_in_usdt: float
    transaction_in_usdt: float
    block_height: int
    decimals: int
    from_address: str
    created_at: datetime
    data: Optional[str]
    cycle: Optional[int]
    class Config:
        orm_mode = True
