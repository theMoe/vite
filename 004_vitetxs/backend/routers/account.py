from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import get_token_header
from nodeFunctions import get_node_ip, get_url, get_header
import requests

router = APIRouter(
    prefix="/account",
    tags=["account"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get('/quota/{viteAddress}', description='Returns quota and vite amount for address')
async def get_quota(viteAddress: str):
    nodeIP = get_node_ip()
    if nodeIP == False:
        print('Connection ERROR...')
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail='Could not find a node')

    url = get_url(nodeIP)
    header = get_header()
    body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "contract_getQuotaByAccount",
        "params": [viteAddress]
    }

    try:
        response = requests.post(url=url, json=body, headers=header)
        response2 = requests.get(url=f'https://vitex.vite.net/reward/pledge/full/list?address={viteAddress}')
        account_info = await get_account_info(viteAddress)
        if response.status_code == status.HTTP_200_OK:
            resp = response.json()
            if not 'result' in resp:
                raise Exception('No data received')
            quota = resp['result']['maxQuota']
            currentQuota = resp['result']['currentQuota']
            stakeAmountQuota = resp['result']['stakeAmount']
            vite_amount = account_info['balanceInfoMap']['tti_5649544520544f4b454e6e40']['balance'] or 0
            pledgedata = response2.json()['data']
            pledge_infos = pledgedata['fullNodePledgeInfos'] if pledgedata is not None else None
            stakedVite = sum(float(x['amount']) / 10**18 for x in pledge_infos) if pledge_infos is not None else 0

            basic = {
                'viteBalance': float(vite_amount) / 10**18,
                'quota': int(quota) / 21000,
                'maxQuota': quota,
                'currentQuota': currentQuota,
                'stakeAmountQuota': float(stakeAmountQuota) / 10**18,
                'stakedVite': stakedVite
            }
            return basic
        else:
            raise HTTPException(status_code=response.status_code)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=e)

@router.get('/tokens/{viteAddress}', description='Returns information about a VITE address (account), e.g. balances of existing tokens, number of account blocks.')
async def get_account_info(viteAddress: str):
    nodeIP = get_node_ip()
    if nodeIP == False:
        print('Connection ERROR...')
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail='Could not find a node')

    url = get_url(nodeIP)
    header = get_header()
    body = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "ledger_getAccountInfoByAddress",
        "params": [viteAddress]
    }

    try:
        response = requests.post(url=url, json=body, headers=header)
        if response.status_code == status.HTTP_200_OK:
            resp = response.json()
            if not 'result' in resp:
                raise Exception('No data received')
            balance_info_map = resp['result']['balanceInfoMap'].values()
            token_list = []
            for each in balance_info_map:
                symbol = each['tokenInfo']['tokenSymbol']
                decimals = each['tokenInfo']['decimals']
                token_index = each['tokenInfo']['index']
                amount = float(each['balance']) / 10**decimals

                if (symbol not in ['VITE', 'VX', 'VCP']):
                    symbol = symbol + '-' + \
                        '{:03}'.format(token_index)

                if amount > 0:
                    usd_value = 0
                    if (symbol != 'USDT'):
                        try:
                            value_request_json = requests.get(
                                        f'https://api.vitex.net/api/v2/exchange-rate?tokenSymbols={symbol}').json()['data'][0]
                            usd_rate = value_request_json['usdRate']
                            usd_value = float(amount) * float(usd_rate)
                        except:
                            print('maybe illegal symbol')
                    else:
                        usd_value = float(amount) * 1

                    usd_value = round(usd_value, 2)

                    available_token = {"symbol": symbol, "amount": amount, "usdt_value": usd_value}
                    token_list.append(available_token)
            token_list.sort(key = lambda json: json['usdt_value'], reverse=True)
            return token_list
        else:
            raise HTTPException(status_code=response.status_code)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=e)


@router.get('/info/{viteAddress}', description='Returns information about a VITE address (account), e.g. balances of existing tokens, number of account blocks.')
async def get_account_info(viteAddress: str):
    nodeIP = get_node_ip()
    if nodeIP == False:
        print('Connection ERROR...')
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail='Could not find a node')

    url = get_url(nodeIP)
    header = get_header()
    body = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "ledger_getAccountInfoByAddress",
        "params": [viteAddress]
    }

    try:
        response = requests.post(url=url, json=body, headers=header)
        if response.status_code == status.HTTP_200_OK:
            resp = response.json()
            if not 'result' in resp:
                raise Exception('No data received')
            print(resp)
            return resp['result']
        else:
            raise HTTPException(status_code=response.status_code)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=e)

@router.get('/staking/{viteAddress}', description='Returns staking details for address')
async def get_quota(viteAddress: str):
    nodeIP = get_node_ip()
    if nodeIP == False:
        print('Connection ERROR...')
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail='Could not find a node')

    url = get_url(nodeIP)
    header = get_header()
    body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "contract_getStakeList",
        "params": [viteAddress, 0, 100]
    }

    try:
        response = requests.post(url=url, json=body, headers=header)
        if response.status_code == status.HTTP_200_OK:
            resp = response.json()
            if not 'result' in resp:
                raise Exception('No data received')

            return resp['result']
        else:
            raise HTTPException(status_code=response.status_code)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=e)

@router.get('/blocks', description='Returns a list of account blocks')
async def getAccountBlocks(viteAddress: str, hash: str, tokenTypeID: str, blocks: int):
    node_ip = get_node_ip()
    if node_ip == False:
        print('Connection ERROR...')
        return {'errorMsg': 'Connection error...'}

    url = get_url(node_ip)
    header = get_header()
    body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "ledger_getAccountBlocks",
        "params": [viteAddress, hash, tokenTypeID, blocks]
    }

    try:
        response = requests.post(url=url, json=body, headers=header)
        if response.status_code == 200:
            resp = response.json()
            if not 'result' in resp:
                return {'errorMsg': 'No data received'}
            if len(resp['result']) == 0:
                return {'errorMsg': 'No token details received'}

            return resp['result']
        else:
            return {'errorMsg': response.status_code}
    except Exception as e:
        print(e)
        return {'errorMsg': 'Exception during request.'}
