from datetime import datetime, timezone
from database.repositories.transactionsrepository import get_transaction_by_viteaddress
from database.models.cyclemodel import Cycle
from database.repositories.cyclesrepository import get_node_status_between_cycles, get_node_status_by_cycle, get_cycle, get_node_status_by_cycle_for_address
from starlette.status import HTTP_200_OK, HTTP_504_GATEWAY_TIMEOUT
from database.repositories.fullnoderepository import get_node_geolocations, get_node_status_from_vite_api
from database.models.node_status_model import NodeStatus
from database.repositories.dailyrewardsrepository import get_dailyreward_by_cycles, get_dailyrewards, get_limited_dailyrewards
from database.models import SessionLocal, get_db
from database.models.dailyrewardmodel import DailyFullNodeRewardOut
from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import get_token_header
from typing import List, Optional
import requests

router = APIRouter(
    prefix="/fullnode",
    tags=["fullnode"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get('/cycleByAddress/{cycle}/{viteAddress}', description='Returns status of the notes related to the given cycle', response_model=List[Cycle])
async def get_cycle_status(viteAddress: str, cycle: int, db: SessionLocal = Depends(get_db)):
    return await get_node_status_by_cycle_for_address(db, cycle, viteAddress)

@router.get('/cycle/{cycle}', description='Returns a list of all active nodes with online ratio and IP for each cycle.')
async def get_fullnode_cycle(cycle: int, db: SessionLocal = Depends(get_db)):
    try:
        db_cycle = await get_cycle(db, cycle)
        if len(db_cycle) > 0:
            return db_cycle
        
        else:
            api_url = 'https://rewardapi.vite.net/reward/full/real'
            params = {'cycle': cycle}
            response = requests.get(url=api_url, params=params)

            if response.status_code == status.HTTP_200_OK:
                resp = response.json()

                if (resp['data'] is None or len(resp['data']) == 0):
                    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                                        detail='No data received')
                nodes = []
                for node in resp['data']:
                    n = {
                        "ip": node['ip'],
                        "address": node['address'],
                        "online_ratio": node['onlineRatio'] * 100,
                        "node_name": node['nodeName']
                    }
                    nodes.append(n)

                return nodes

            else:
                raise HTTPException(status_code=response.status_code)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get('/cycleToDB/{cycle}', description='Returns a list of all active nodes with online ratio and IP for each cycle.')
async def get_fullnode_cycle_from_viteapi(cycle: int, getAlive: bool):
    try:
        api_url = 'https://rewardapi.vite.net/reward/full/real'
        params = {'cycle': cycle}
        response = requests.get(url=api_url, params=params)

        if response.status_code == status.HTTP_200_OK:
            resp = response.json()
            
            if (resp['data'] is None or len(resp['data']) == 0):
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                                    detail='No data received')

            if getAlive:
                requested_addresses = {}
                for node in resp['data']:
                    node['isAlive'] = False
                    node['version'] = None
                    node['height'] = None
                    node['msg'] = 'No information available'

                    if node['address'] in requested_addresses.keys():
                        for aliveNode in requested_addresses[node['address']]:
                            if aliveNode['ip'] == node['ip']:
                                if 'nodeName' in aliveNode:
                                    node['nodeName'] = aliveNode['nodeName']
                                if 'isAlive' in aliveNode:
                                    node['isAlive'] = aliveNode['isAlive']
                                else:
                                    node['isAlive'] = False
                                if 'version' in aliveNode:
                                    node['version'] = aliveNode['version']
                                else:
                                    node['version'] = None
                                if 'height' in aliveNode:
                                    node['height'] = aliveNode['height']
                                else:
                                    node['height'] = None
                                if 'msg' in aliveNode:
                                    node['msg'] = aliveNode['msg']
                                else:
                                    node['msg'] = None

                                del aliveNode
                    else:
                        addr = node['address']
                        url = f'https://stats.vite.net/api/getAlivePeers?address={addr}'

                        response = requests.get(url, timeout=10)
                        if (response.status_code is status.HTTP_200_OK):
                            getAliveResp = response.json()
                            if 'list' in getAliveResp:
                                
                                if len(getAliveResp['list']) == 0:
                                    node['isAlive'] = False
                                    node['version'] = None
                                    node['height'] = None
                                    node['msg'] = 'No information available'
                                else:
                                    requested_addresses[addr] = getAliveResp['list']
                                    for aliveNode in requested_addresses[addr]:
                                        if aliveNode['ip'] == node['ip']:
                                            if 'nodeName' in aliveNode:
                                                node['nodeName'] = aliveNode['nodeName']
                                            if 'isAlive' in aliveNode:
                                                node['isAlive'] = aliveNode['isAlive']
                                            else:
                                                node['isAlive'] = False
                                            if 'version' in aliveNode:
                                                node['version'] = aliveNode['version']
                                            else:
                                                node['version'] = None
                                            if 'height' in aliveNode:
                                                node['height'] = aliveNode['height']
                                            else:
                                                node['height'] = None
                                            if 'msg' in aliveNode:
                                                node['msg'] = aliveNode['msg']
                                            else:
                                                node['msg'] = None

                                            del aliveNode
            return resp['data']

        else:
            raise HTTPException(status_code=response.status_code)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get('/rewards', status_code=status.HTTP_200_OK, response_model=List[DailyFullNodeRewardOut])
async def get_all_reward_data(limit: Optional[int], db: SessionLocal = Depends(get_db)):
    if limit is None:
        return await get_dailyrewards(db)
    else:
        return await get_limited_dailyrewards(db, limit)

@router.get('/status/basic/{cycle_offset}')
async def get_basic_node_stats(cycle_offset: int, db: SessionLocal = Depends(get_db)):
    def condition(nodeStatus: NodeStatus):
        return nodeStatus.online_ratio >= 0.9
    
    if cycle_offset <= 0:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail='Offset must be >0')
    
    cycle_offset = cycle_offset - 1

    dt = datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    current_cycle = int((utc_timestamp - 1558411200) / 24 / 3600) - 1 
    offset_cycle = current_cycle - cycle_offset
    double_offset_cycle = current_cycle - (cycle_offset * 2) - 1
    requested_cycles = await get_node_status_between_cycles(db, offset_cycle, current_cycle)
    requested_active = sum(condition(x) for x in requested_cycles) / (cycle_offset + 1)
    previous_cycles = await get_node_status_between_cycles(db, double_offset_cycle, offset_cycle - 1)
    previous_active = sum(condition(x) for x in previous_cycles) / (cycle_offset + 1)
    requested_cycles_num = set(list(map(lambda each: each.cycle, requested_cycles)))
    previous_cycles_num = set(list(map(lambda each: each.cycle, previous_cycles)))
    requested_rewards = await get_dailyreward_by_cycles(db, requested_cycles_num)
    previous_rewards = await get_dailyreward_by_cycles(db, previous_cycles_num)
    requested_rewards_sum = sum(x.amount_normalised for x in requested_rewards)  / (cycle_offset + 1)
    previous_rewards_sum = sum(x.amount_normalised for x in previous_rewards) / (cycle_offset + 1)

    response = {"current_timespan": {
                    "nodes": len(requested_cycles) / (cycle_offset + 1), 
                    "active": requested_active,
                    "rewards": requested_rewards_sum},
                    "last_timespan": {
                        "nodes": len(previous_cycles) / (cycle_offset + 1), 
                        "active": previous_active, 
                        "rewards": previous_rewards_sum}
                }
    return response

@router.get('/transactions/{viteAddress}')
async def get_transactions_for_address(viteAddress: str, db: SessionLocal = Depends(get_db)):
    return await get_transaction_by_viteaddress(db, viteAddress)

@router.get('/alivepeers/{viteAddress}', description='Returns the living nodes depending on the vite address.')
async def get_alive_peers(viteAddress: str):
    try:
        api_url = 'https://stats.vite.net/api/getAlivePeers'
        params = {'address': viteAddress}
        response = requests.get(url=api_url, params=params)

        if response.status_code == status.HTTP_200_OK:
            resp = response.json()
            if (resp['size'] == 0):
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                                    detail='No data received')
            return resp['list']
        else:
            raise HTTPException(status_code=response.status_code)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get('/status/{cycle}/{viteAddress}', status_code=status.HTTP_200_OK, response_model=List[NodeStatus])
async def get_live_node_status(viteAddress: str, cycle: int, db: SessionLocal = Depends(get_db)):
    try:
        return await get_node_status_from_vite_api(viteAddress, cycle, db)
    except:
        raise HTTPException(status_code=HTTP_504_GATEWAY_TIMEOUT,
                            detail='Vite API is not available')


@router.get('/geolocations', status_code=HTTP_200_OK)
async def get_geolocations(db: SessionLocal = Depends(get_db)):
    return await get_node_geolocations(db)