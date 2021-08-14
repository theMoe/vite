from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import get_token_header
from nodeFunctions import get_url, get_header
import requests

router = APIRouter(
    prefix="/net",
    tags=["net"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get('/syncinfo/{ip}', description='Returns sync info for a node.')
async def load_syncInfo(ip: str):
    return await load_net(ip, 'net_syncInfo')

@router.get('/syncdetail/{ip}', description='Returns sync details for a node.')
async def load_syncDetail(ip: str):
    return await load_net(ip, 'net_syncDetail')

@router.get('/nodeinfo/{ip}', description='Return the detailed information of current Node.')
async def load_nodeInfo(ip: str):
    return await load_net(ip, 'net_nodeInfo')

async def load_net(ip: str, method: str):
    node_ip = ip

    url = get_url(node_ip)
    header = get_header()
    body = {"jsonrpc": "2.0", "id": 2, "method": method, "params": None}

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