from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from dependencies import get_token_header
from file_generating_service import generate_return_file_msg
from typing import Optional, List
from nodeFunctions import get_node_ip, get_url, get_header
from database.models.sbp_votes import SBPVotes
from typing import Optional

import requests

router = APIRouter(
    prefix="/sbp",
    tags=["sbp"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get('/', description='Returns a list of block producer nodes')
async def get_sbp(node_ip: Optional[str] = None, sbp_details: Optional[bool] = True):
    if node_ip == None:
        node_ip = get_node_ip()
    dt = datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    last_cycle = int((utc_timestamp - 1558411200) / 24 / 3600) -1

    if node_ip == False:
        print('Connection ERROR...')
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail='No nodes available.')

    url = get_url(node_ip)
    header = get_header()
    body = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "contract_getSBPVoteList",
        "params": None
    }

    try:
        response = requests.post(url=url, json=body, headers=header)
        if response.status_code == status.HTTP_200_OK:
            resp = response.json()
            if not 'result' in resp or len(resp['result']) == 0:
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                                    detail='No data received')
            if sbp_details:
                sbp_cycle = (await get_sbp_reward_by_cycle(last_cycle, node_ip))['result']['rewardMap']

                modified_response = []
                for e in resp['result']:
                    name = e['sbpName']
                    node_in_cycle = sbp_cycle[name]

                    sbp = SBPVotes.parse_obj({
                        'sbp_name': name, 
                        'block_producing_address': e['blockProducingAddress'],
                        'votes': e['votes'][:len(e['votes']) - 18],
                        'count': node_in_cycle['producedBlocks'],
                        'ratio': (float(node_in_cycle['producedBlocks']) / float(node_in_cycle['targetBlocks'])) * 100,
                        'block_creation_rewards': float(node_in_cycle['blockProducingReward']) / 10**18,
                        'rewards_of_votes': float(node_in_cycle['votingReward']) / 10**18,
                        'rewards_in_total': float(node_in_cycle['totalReward']) / 10**18,
                    })
                    modified_response.append(sbp)            
                return modified_response
            else:
                return resp['result']
        else:
            raise HTTPException(status_code=response.status_code)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# {
#   "jsonrpc": "2.0",
#   "id": 2,
#   "result": {
#     "rewardMap": {
#       "BEPAL": {
#         "blockProducingReward": "174086757990867579885",
#         "votingReward": "266560703858666129823",
#         "totalReward": "440647461849533709708",
#         "producedBlocks": "366",
#         "targetBlocks": "366",
#         "allRewardWithdrawed": false
#       }, ...
#     },
#     "startTime": 1575691200,
#     "endTime": 1575777600,
#     "cycle": "200"
#   }
# }
# https://vite.wiki/api/rpc/contract_v2.html#contract_getsbprewardbycycle
@router.get('/rewards/{cycle}', description='Return SBP rewards of all SBP nodes by cycle')
async def get_sbp_reward_by_cycle(cycle: int, node_ip: Optional[str] = None):
    if node_ip == None:
        node_ip = get_node_ip()
    if node_ip == False:
        print('Connection ERROR...')
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail='No nodes available.')

    url = get_url(node_ip)
    header = get_header()
    body = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "contract_getSBPRewardByCycle",
        "params": [str(cycle)]
    }

    try:
        response = requests.post(url=url, json=body, headers=header)
        if response.status_code == status.HTTP_200_OK:
            resp = response.json()
            if not 'result' in resp or len(resp['result']) == 0:
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                                    detail='No data received')
        
            return resp
        else:
            raise HTTPException(status_code=response.status_code)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 1627692639
# {
#   "jsonrpc": "2.0",
#   "id": 2,
#   "result": {
#     "rewardMap": {
#       "AnkrSupernodeVite": {
#         "blockProducingReward": "0",
#         "votingReward": "0",
#         "totalReward": "0",
#         "producedBlocks": "0",
#         "targetBlocks": "492",
#         "allRewardWithdrawed": false
#       },
#       "Beauty.Vite": {
#         "blockProducingReward": "1498287671232876712125",
#         "votingReward": "917762162595239641249",
#         "totalReward": "2416049833828116353374",
#         "producedBlocks": "3150",
#         "targetBlocks": "3156",
#         "allRewardWithdrawed": false
#       },
#       ...
#     },
#     "startTime": 1627617600,
#     "endTime": 1627704000,
#     "cycle": "801"
#   }
# }
# https://vite.wiki/api/rpc/contract_v2.html#contract_getsbprewardbytimestamp
@router.get('/rewards24h/{timestamp}', description='Return SBP rewards in 24h by timestamp. Rewards of all SBP nodes in the cycle that the given timestamp belongs will be returned.')
async def get_sbp_reward_by_timestamp(timestamp: int):
    node_ip = get_node_ip()
    if node_ip == False:
        print('Connection ERROR...')
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail='No nodes available.')

    url = get_url(node_ip)
    header = get_header()
    body = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "contract_getSBPRewardByTimestamp",
        "params": [timestamp]
    }

    try:
        response = requests.post(url=url, json=body, headers=header)
        if response.status_code == status.HTTP_200_OK:
            resp = response.json()
            if not 'result' in resp or len(resp['result']) == 0:
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                                    detail='No data received')
        
            return resp
        else:
            raise HTTPException(status_code=response.status_code)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# {
#   "jsonrpc": "2.0",
#   "id": 2,
#   "result": {
#     "name": "Beauty.Vite",
#     "blockProducingAddress": "vite_aa7f76480db9e4072231d52f7b7abcccc8197b217a2dd5e818",
#     "rewardWithdrawAddress": "vite_f3593e633218ba13b2a6a6379d87e588285a5fba778dd3c20c",
#     "stakeAddress": "vite_f3593e633218ba13b2a6a6379d87e588285a5fba778dd3c20c",
#     "stakeAmount": "500000000000000000000000",
#     "expirationHeight": "7776000",
#     "expirationTime": 1567716098,
#     "revokeTime": 0
#   }
# }
# https://vite.wiki/api/rpc/contract_v2.html#contract_getsbp
@router.get('/sbp/{sbpName}', description='Return SBP node information')
async def get_sbp_reward_by_timestamp(sbpName: str):
    node_ip = get_node_ip()
    if node_ip == False:
        print('Connection ERROR...')
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail='No nodes available.')

    url = get_url(node_ip)
    header = get_header()
    body = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "contract_getSBP",
        "params": [sbpName]
    }

    try:
        response = requests.post(url=url, json=body, headers=header)
        if response.status_code == status.HTTP_200_OK:
            resp = response.json()
            if not 'result' in resp or len(resp['result']) == 0:
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                                    detail='No data received')
        
            return resp
        else:
            raise HTTPException(status_code=response.status_code)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get('/votes/{cycle}', description='Returns a CSV of all SBPs with a list of voters per SBP')
async def get_vote_details_by_cycle(cycle: int, blockProducerNames: Optional[List[str]] = Query(None)):
    node_ip = get_node_ip()
    if node_ip == False:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail='No nodes available.')

    url = get_url(node_ip)
    header = get_header()
    body = get_body(cycle)

    results = []

    try:
        response = requests.post(url=url, json=body, headers=header)

        if response.status_code == status.HTTP_200_OK:
            resp = response.json()
            for result in resp['result']:
                print(result)
                block_producer_name = result['blockProducerName']
                if (blockProducerNames == None or block_producer_name in blockProducerNames):
                    for key, value in result['addressVoteMap'].items():
                        data = {
                            'cycle': cycle,
                            'blockProducerName': block_producer_name,
                            'voteAddress': key,
                            'votes': value,
                            'votesDecimals': float(value) / 10**18
                        }
                        results.append(data)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Exception during request.')

    if len(results) > 0:
        generated_message = generate_return_file_msg(results)
        response = StreamingResponse(content=generated_message['file'],
                                     media_type='text/csv',
                                     headers={'Content-Disposition': 'filename=sbpVoteDetails_{cycle}.csv'})
        return response
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail='No transactions available')


def get_body(cycle):
    body = {
        'jsonrpc': '2.0',
        'id': 2,
        'method': 'contract_getSBPVoteDetailsByCycle',
        'params': [str(cycle)]
    }
    return body
