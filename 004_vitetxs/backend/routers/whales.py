from typing import List, Optional
from starlette.status import HTTP_200_OK
from database.models.whalemodel import WhaleChange, WhaleOut
from database.models import SessionLocal, get_db
from fastapi import APIRouter, Depends, status
from dependencies import get_token_header
from database.repositories.whalesrepository import get_last_whales, get_top_whale_addresses, get_top_whales, get_whale_count_by_days, get_whales_group_by_week, get_whales_ratio_by_day


router = APIRouter(
    prefix="/whales",
    tags=["whales"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[WhaleOut])
async def get_whale_data(limit: Optional[int] = 1000, db: SessionLocal = Depends(get_db)):
    return await get_last_whales(db, limit)

@router.get('/top', status_code=status.HTTP_200_OK, response_model=List[WhaleOut])
async def get_top_whale_data(limit: Optional[int] = 10, db: SessionLocal = Depends(get_db)):
    return await get_top_whales(db, limit)

@router.get('/change', status_code=HTTP_200_OK, response_model=WhaleChange)
async def get_period_change_data(days: int, db: SessionLocal = Depends(get_db)):
    current = await get_whale_count_by_days(db, days)
    previous = await get_whale_count_by_days(db, days * 2)

    return WhaleChange(current=current, previous=previous)

@router.get('/topaddress', status_code=HTTP_200_OK)
async def get_top_whale_by_address(db: SessionLocal = Depends(get_db)):
    return await get_top_whale_addresses(db)

@router.get('/sumbyday', status_code=HTTP_200_OK)
async def get_whales_ratio_by_days(db: SessionLocal = Depends(get_db)):
    return await get_whales_ratio_by_day(db)

@router.get('/byWeek', status_code=HTTP_200_OK)
async def get_whales_by_week(db: SessionLocal = Depends(get_db)):
    return await get_whales_group_by_week(db)
