import datetime
from typing import List

from sqlalchemy.sql.expression import desc
from database.models.transactionmodel import DBTransaction, TransactionOut
from sqlalchemy.orm import Session
from sqlalchemy import or_

async def get_transaction_by_viteaddress(db: Session, vite_address: str) -> List[TransactionOut]:
    dbtrans = db.query(DBTransaction).filter(or_(DBTransaction.to_address == vite_address, DBTransaction.from_address == vite_address)).order_by(desc(DBTransaction.timestamp)).all()
    transout = []
    for each in dbtrans:
        out = TransactionOut()
        out.amount = each.amount
        out.amount_normalised = float(each.amount) / 10**each.decimals
        out.block_height = each.account_block_height
        out.created_at = each.timestamp
        out.decimals = each.decimals
        out.from_address = each.from_address
        out.status = "sent" if each.block_type == 2 else "received"
        out.snapshot_hash = each.first_snapshot_hash
        out.symbol = each.token_symbol
        out.to_address = each.to_address
        out.token_id = each.token_id
        out.tx_hash = each.hash
        transout.append(out)
    return transout

async def get_all_transactions(limit: int, db: Session) -> List[TransactionOut]:
    dbtrans = db.query(DBTransaction).order_by(desc(DBTransaction.timestamp)).limit(limit).all()
    transout = []
    for each in dbtrans:
        out = TransactionOut()
        out.amount = each.amount
        out.amount_normalised = float(each.amount) / 10**each.decimals
        out.block_height = each.account_block_height
        out.created_at = each.timestamp
        out.decimals = each.decimals
        out.from_address = each.from_address
        out.status = "sent" if each.block_type == 2 else "received"
        out.snapshot_hash = each.first_snapshot_hash
        out.symbol = each.token_symbol
        out.to_address = each.to_address
        out.token_id = each.token_id
        out.tx_hash = each.hash
        transout.append(out)
    return transout

async def get_last_transaction(db: Session) -> DBTransaction:
    return db.query(DBTransaction).order_by(desc(DBTransaction.timestamp)).first()

async def get_transaction_count_since_last_day(db: Session) -> int:
    today = datetime.datetime.now()
    target_date = today - datetime.timedelta(hours=24)
    return db.query(DBTransaction).filter(DBTransaction.timestamp > target_date).count()

async def get_disctinct_accounts_by_transaction(db: Session) -> int:
    return db.query(DBTransaction).distinct(DBTransaction.to_address).count()

async def create_transaction(db: Session, dr: DBTransaction):
    db.add(dr)
    db.commit()
    db.refresh(dr)

    return dr

