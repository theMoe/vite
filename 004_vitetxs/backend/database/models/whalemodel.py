from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, Numeric
from sqlalchemy.sql.schema import Table
from sqlalchemy.types import DateTime
from datetime import datetime
from database.models import Base

class DBWhale(Base):
    __tablename__ = "Whales"

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
    transaction_in_usdt = Column(Float, index=True)
    block_height = Column(Integer)
    decimals = Column(Integer)
    from_address = Column(String(255))
    to_address = Column(String(255))
    data = Column(String(255))

class WhaleOut(BaseModel):
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
    to_address: str
    created_at: datetime
    data: Optional[str]
    class Config:
        orm_mode = True

class WhaleIn(BaseModel):
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
    to_address: str
    created_at: datetime
    data: Optional[str]
    class Config:
        orm_mode = True

class WhaleChange(BaseModel):
    current: List[float]
    previous: List[float]

class WhaleTransactionsStats(Base):
     __table__ = Table('WhaleTransactionsStats', Base.metadata,
        Column('address', String(255), primary_key=True),
        Column('transaction_type', String(255)),
        Column('total_sum_in_usdt', Float),
        Column('total_transactions', Integer),
        Column('count_small', Integer),
        Column('count_medium', Integer),
        Column('count_big', Integer))