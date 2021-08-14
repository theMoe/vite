import json
import math
import time
import requests

from database.repositories.locationrepository import create_location
from database.models.locationmodel import DBLocation
from database.models.whalemodel import WhaleIn, DBWhale
from database.models.dailyrewardmodel import DBDailyFullNodeReward, DailyFullNodeRewardIn
from database.models.cyclemodel import Cycle
from database.models import SessionLocal, get_db
from fastapi import APIRouter, Depends, status, Body
from dependencies import get_hook_token_header
from database.repositories.whalesrepository import create_whale
from database.repositories.dailyrewardsrepository import create_dailyreward
from database.repositories.cyclesrepository import create_cycle, get_distinct_ips_from_cycles, update_current_cycle
from routers.fullnode import get_fullnode_cycle_from_viteapi
from datetime import datetime, timezone

router = APIRouter(
    prefix="/webhook",
    tags=["webhook"],
    dependencies=[Depends(get_hook_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.post('/whale', status_code=status.HTTP_200_OK, response_model=WhaleIn)
async def consume_whale_data(whale: WhaleIn = Body(...), db: SessionLocal = Depends(get_db)):
    print("consume whale data")
    db_whale = DBWhale()
    db_whale.created_at = whale.created_at
    db_whale.symbol = whale.symbol
    db_whale.token_id = whale.token_id
    db_whale.tweet_id = whale.tweet_id
    db_whale.tx_hash = whale.tx_hash
    db_whale.snapshot_hash = whale.snapshot_hash
    db_whale.amount = whale.amount
    db_whale.amount_normalised = whale.amount / math.pow(10, whale.decimals)
    db_whale.token_in_usdt = whale.token_in_usdt
    db_whale.transaction_in_usdt = whale.transaction_in_usdt
    db_whale.block_height = whale.block_height
    db_whale.decimals = whale.decimals
    db_whale.from_address = whale.from_address
    db_whale.to_address = whale.to_address
    db_whale.data = whale.data
    foo = await create_whale(db, db_whale)
    return foo

@router.post('/dailyReward', status_code=status.HTTP_200_OK, response_model=DailyFullNodeRewardIn)
async def consume_daily_reward_data(dr: DailyFullNodeRewardIn = Body(...), db: SessionLocal = Depends(get_db)):
    db_full_node_reward = DBDailyFullNodeReward()
    db_full_node_reward.created_at = dr.created_at
    db_full_node_reward.symbol = dr.symbol
    db_full_node_reward.token_id = dr.token_id
    db_full_node_reward.tweet_id = dr.tweet_id
    db_full_node_reward.tx_hash = dr.tx_hash
    db_full_node_reward.snapshot_hash = dr.snapshot_hash
    db_full_node_reward.amount = dr.amount
    db_full_node_reward.amount_normalised = dr.amount / math.pow(10, dr.decimals)
    db_full_node_reward.token_in_usdt = dr.token_in_usdt
    db_full_node_reward.transaction_in_usdt = dr.transaction_in_usdt
    db_full_node_reward.block_height = dr.block_height
    db_full_node_reward.decimals = dr.decimals
    db_full_node_reward.from_address = dr.from_address
    db_full_node_reward.data = dr.data
    db_full_node_reward.cycle = dr.cycle
    foo = await create_dailyreward(db, db_full_node_reward)
    return foo


@router.post('/cycle', status_code=status.HTTP_200_OK, response_model=Cycle)
async def consume_cycle(dr: Cycle = Body(...), db: SessionLocal = Depends(get_db)):
    print(dr)
    foo = await create_cycle(db, dr)
    return foo


@router.post('/cycleBatch', status_code=status.HTTP_200_OK, response_model=Cycle)
async def cycle_batch(fromCycle: int, toCycle: int, getAlive: bool, db: SessionLocal = Depends(get_db)):
    if (toCycle < fromCycle):
        return "toCycle < from Cycle"

    for cycle in range(fromCycle, toCycle + 1):
        try:
            cycle_data = await get_fullnode_cycle_from_viteapi(cycle, getAlive)

            if (len(cycle_data) > 0):
                dt = datetime.now(timezone.utc)
                utc_time = dt.replace(tzinfo=timezone.utc)
                utc_timestamp = utc_time.timestamp()

                print('Start', cycle, 'Nodes', len(cycle_data))
                data_dt = datetime.utcfromtimestamp(utc_timestamp)
                
                for node in cycle_data:
                    if 'isAlive' not in node and 'version' not in node and 'height' not in node and 'msg' not in node:
                        node['isAlive'] = False
                        node['version'] = None
                        node['height'] = None
                        node['msg'] = 'No information available'

                    node_data = Cycle.parse_obj({
                        'cycle': cycle,
                        'created_at': data_dt,
                        'ip': node['ip'],
                        'address': node['address'],
                        'node_name': node['nodeName'],
                        'online_ratio': node['onlineRatio'],
                        'isAlive': node['isAlive'],
                        'version': node['version'],
                        'height': node['height'],
                        'msg': node['msg']
                    })

                    await update_current_cycle(db, node_data)
                print('Done', cycle, 'Nodes', len(cycle_data))
        except Exception as e:
            print(e)

@router.get('/fetchIPlocations')
async def fetch_ip_locations(db: SessionLocal = Depends(get_db)):
    geo_ip = 'http://ip-api.com/batch?fields=58623'
    cycles = await get_distinct_ips_from_cycles(db)

    def split(a, n):
        k, m = divmod(len(a), n)
        return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

    splittet = split(cycles, 2)

    for each in splittet:
        params = []
        for ip in each:
            params.append(ip.ip)
        
        try:
            response = requests.post(url=geo_ip, data=json.dumps(params))
            if response.status_code == status.HTTP_200_OK:
                resp = response.json()
                for resolve in resp:
                    if resolve['status'] == 'success':
                        db_location = DBLocation()
                        db_location.ip = resolve["query"]
                        db_location.org = resolve["org"]
                        db_location.lat = resolve["lat"]
                        db_location.lon = resolve["lon"]
                        db_location.region = resolve["region"]
                        db_location.region_name = resolve["regionName"]
                        db_location.city = resolve["city"]
                        db_location.country = resolve["country"]
                        db_location.country_code = resolve["countryCode"]
                        db_location.zip = resolve["zip"]

                        await create_location(db, db_location)

        except Exception as e:
            print(e)
        time.sleep(60)
