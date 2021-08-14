from fastapi import APIRouter, Depends
from starlette import status
from dependencies import get_token_header
from nodeFunctions import get_node_ip, get_url, get_header
import requests
from typing import Optional

router = APIRouter(
    prefix="/tokens",
    tags=["tokens"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get('/list', description='Returns a list of all tokens')
async def get_token_info_list(node_ip: Optional[str] = None):
    if node_ip == None:
        node_ip = get_node_ip()
    if node_ip == False:
        print('Connection ERROR...')
        return {'errorMsg': 'Connection error...'}

    url = get_url(node_ip)
    header = get_header()
    body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "contract_getTokenInfoList",
        "params": [0, 500]
    }

    try:
        response = requests.post(url=url, json=body, headers=header)
        if response.status_code == status.HTTP_200_OK:
            resp = response.json()
            #print(resp)
            if not 'result' in resp:
                return {'errorMsg': 'No data received'}
            if len(resp['result']) == 0:
                return {'errorMsg': 'No token details received'}
            token_info_list = resp['result']['tokenInfoList']
            requested_list = []
            for element in token_info_list:
                requested_list.append({
          "tokenName": element['tokenName'],
          "tokenSymbol": element['tokenSymbol'],
          "totalSupply": float(element['totalSupply']) / 10**element['decimals'],
          "decimals": element['decimals'],
          "owner": element['owner'],
          "tokenId": element['tokenId'],
          "maxSupply": element['maxSupply'],
          "ownerBurnOnly": element['ownerBurnOnly'],
          "isReIssuable": element['isReIssuable'],
          "index": element['index'],
          "isOwnerBurnOnly": element['isOwnerBurnOnly']
        })
            
            return requested_list
        else:
            return {'errorMsg': response.status_code}
    except Exception as e:
        print(e)
        return {'errorMsg': 'Exception during request.'}


@router.get('/details/{tokenID}', description='Determination of token information on the basis of the tokenID')
async def get_token_info_by_id(tokenID: str):
    node_ip = get_node_ip()
    if node_ip == False:
        print('Connection ERROR...')
        return {'errorMsg': 'Connection error...'}

    url = get_url(node_ip)
    header = get_header()
    body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "contract_getTokenInfoById",
        "params": tokenID
    }

    try:
        response = requests.post(url=url, json=body, headers=header)
        if response.status_code == status.HTTP_200_OK:
            resp = response.json()
            if not 'result' in resp:
                return {'errorMsg': 'No data received'}
            if len(resp['result']) == 0:
                return {'errorMsg': 'No token details received'}

            return {'data': resp}
        else:
            return {'errorMsg': response.status_code}
    except Exception as e:
        print(e)
        return {'errorMsg': 'Exception during request.'}
