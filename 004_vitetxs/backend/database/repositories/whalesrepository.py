import datetime
from typing import List
from sqlalchemy.orm.query import Query
from sqlalchemy.sql.expression import desc
from ..models.whalemodel import DBWhale, WhaleTransactionsStats
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

""""
All database actions associated with the whale resource
"""
async def get_whales(db: Session):
    return db.query(DBWhale).all()

async def get_whale(db: Session, whale_id: int):
    return db.query(DBWhale).where(DBWhale.id == whale_id).first()

async def get_last_whales(db: Session, limit: int):
    return db.query(DBWhale).order_by(desc(DBWhale.created_at)).limit(limit).all()

async def get_first_whale(db: Session):
    return db.query(DBWhale).order_by(desc(DBWhale.created_at)).first()

async def get_top_whales(db: Session, limit: int):
    return db.query(DBWhale).order_by(desc(DBWhale.transaction_in_usdt)).limit(limit).all()

async def get_top_whale_addresses(db: Session):
    foo = db.query(WhaleTransactionsStats).all()
    j = []
 
    for each in foo:
        if not any(x['address'] == each.address for x in j):
            j.append({"address": each.address,"received": {"count" : {"large": 0,"medium": 0,"small": 0}},
            "sent": {"count" : {"large": 0, "medium": 0, "small": 0}},"sum_usdt_value": 0})

    for each in foo:
        for e in j:
            if each.address == e['address']:
                if each.transaction_type == 'recieved':
                    e['received']['count']['small'] = each.count_small
                    e['received']['count']['medium'] = each.count_medium
                    e['received']['count']['large'] = each.count_big
                if each.transaction_type == 'sent':
                    e['sent']['count']['small'] = each.count_small
                    e['sent']['count']['medium'] = each.count_medium
                    e['sent']['count']['large'] = each.count_big
                e['sum_usdt_value'] =+ each.total_sum_in_usdt
      
    return j
    
async def get_all_whales_by_last_days(db: Session, days: int) -> List[DBWhale]:
    delta_of_days = datetime.now() - datetime.timedelta(hours=24 * days)
    return db.query(DBWhale).filter(DBWhale.created_at > delta_of_days).all()


def __smallFilter(query: Query):
    return query.filter(DBWhale.transaction_in_usdt < 100000.00)


def __mediumFilter(query: Query):
    return query.filter(DBWhale.transaction_in_usdt >= 100000.00).filter(DBWhale.transaction_in_usdt < 500000.00)


def __largeFilter(query: Query):
    return query.filter(DBWhale.transaction_in_usdt >= 500000.00)


async def get_whale_count_by_days(db: Session, days: int):
    delta_of_days = datetime.datetime.now() - datetime.timedelta(hours=24 * days)
    base_query = db.query(DBWhale).filter(DBWhale.created_at > delta_of_days)
    small_count = __smallFilter(base_query).count()
    medium_count = __mediumFilter(base_query).count()
    large_count = __largeFilter(base_query).count()
    return [small_count, medium_count, large_count]


async def get_whales_ratio_by_day(db: Session):
    def __build_query(day: int):
        return db.query(DBWhale).filter(func.extract('dow', DBWhale.created_at) == day)

    small = []
    medium = []
    large = []

    for day in range(6):
        small.append(__smallFilter(__build_query(day + 1)).count())
        medium.append(__mediumFilter(__build_query(day + 1)).count())
        large.append(__largeFilter(__build_query(day + 1)).count())

    first_whale = await get_first_whale(db)
    monday1 = (first_whale.created_at -
               datetime.timedelta(days=first_whale.created_at.weekday()))
    monday2 = (datetime.datetime.now() -
               datetime.timedelta(days=datetime.datetime.now().weekday()))
    number_of_weeks = (monday2 - monday1).days / 7 + 1

    def __get_ratio(single: int) -> float:
        if (number_of_weeks == 0.0):
            return single
        return single / number_of_weeks

    small_ratio = list(map(lambda each: __get_ratio(each), small))
    medium_ratio = list(map(lambda each: __get_ratio(each), medium))
    large_ratio = list(map(lambda each: __get_ratio(each), large))

    return {"small": small_ratio, "medium": medium_ratio, "large": large_ratio}

async def get_whales_group_by_week(db: Session):
    today = datetime.datetime.now()
    target_date = today - datetime.timedelta(weeks=10)
    today_week = date(today.year, today.month, today.day).isocalendar()[1]
    target_week = date(target_date.year, target_date.month, target_date.day).isocalendar()[1]
    data = db.query(DBWhale).filter(DBWhale.created_at > target_date).all()

    j = []

    for e in range(target_week, today_week):
        j.append({
            "calendar_week": e,
            "whale_transactions": {
                "small": 0,
                "medium": 0,
                "large": 0
            }
        })

    for e in data:
        week = date(e.created_at.year, e.created_at.month, e.created_at.day).isocalendar()[1]
        for entry in j:
            if entry['calendar_week'] == week:
                if (e.transaction_in_usdt < 100000.00):
                    entry['whale_transactions']['small'] +=1
                elif (e.transaction_in_usdt >= 100000.00 and e.transaction_in_usdt < 500000.00):
                    entry['whale_transactions']['medium'] +=1
                else:
                    entry['whale_transactions']['large'] +=1

    return j

async def create_whale(db: Session, db_whale: DBWhale):
    db.add(db_whale)
    db.commit()
    db.refresh(db_whale)

    return db_whale
