from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Numeric
from sqlalchemy.types import DateTime
from datetime import datetime
from database.models import Base

class DBTransaction(Base):
    __tablename__ = "Transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    block_type = Column(Integer)
    block_type_description = Column(String(255))
    account_block_height = Column(Integer)
    hash = Column(String(255), index=True)
    account_address = Column(String(255))
    sbp_producer = Column(String(255))
    from_address = Column(String(255), index=True)
    to_address = Column(String(255), index=True)
    amount = Column(Numeric(asdecimal=False))
    fee = Column(Numeric(asdecimal=False))
    data = Column(String(255))
    token_name = Column(String(255))
    token_symbol = Column(String(255))
    decimals = Column(Integer)
    token_id = Column(String(255))
    index = Column(Integer)
    first_snapshot_hash = Column(String(255))
    first_snapshot_height = Column(Integer)
    timestamp = Column(DateTime, index=True)

class Transaction(BaseModel):
    block_type: int
    block_type_description: str
    account_block_height: int
    hash: str
    account_address: str
    sbp_producer: str
    from_address: str
    to_address: str
    amount: int
    fee: int
    data: str
    token_name: str
    token_symbol: str
    decimals: int
    token_id: str
    index: int
    first_snapshot_hash: str
    first_snapshot_height: int
    timestamp: datetime
    class Config:
        orm_mode = True

class TransactionOut:
   amount: int
   amount_normalised: float
   block_height: int
   created_at: datetime
   decimals: int
   from_address: str
   status: str
   snapshot_hash: str
   symbol: str
   to_address: str
   token_id: str
   tx_hash: str