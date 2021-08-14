from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from dependencies import get_token_header, get_dex_api_url
from datetime import datetime, timezone
from file_generating_service import generate_return_file_msg
import requests

router = APIRouter(
    prefix="/mining",
    tags=["mining"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get('/invite/{viteAddress}', description='Returns the earnings that you receive when you have recruited someone.')
async def load_invite_mining_data(viteAddress: str):
    try:
        api_url = get_dex_api_url(1) + '/mining/invite'
        params = {'address': viteAddress}

        response = requests.get(url=api_url, params=params)

        if response.status_code == status.HTTP_200_OK:
            resp = response.json()
            check_response(resp)
            csv_data = build_mining_data_list(resp['data']['miningList'])

            generated_message = generate_return_file_msg(csv_data)
            response = StreamingResponse(content=generated_message['file'],
                                         media_type='text/csv',
                                         headers={'Content-Disposition': 'filename=inviteMining_{viteAddress}.csv'})
            return response
        else:
            raise HTTPException(status_code=response.status_code,
                                detail='Error from vite network')
    except Exception as e:
        raise e


@router.get('/trade/{viteAddress}', description='Returns the earnings that you get from trading tokens.')
async def load_trading_mining_data(viteAddress: str):
    try:
        api_url = get_dex_api_url(1) + '/mining/trade'
        params = {'address': viteAddress}

        response = requests.get(url=api_url, params=params)

        if response.status_code == status.HTTP_200_OK:
            resp = response.json()
            check_response(resp)
            csv_data = build_mining_data_list(resp['data']['miningList'])

            generated_message = generate_return_file_msg(csv_data)
            response = StreamingResponse(content=generated_message['file'],
                                         media_type='text/csv',
                                         headers={'Content-Disposition': 'filename=tradeMining_{viteAddress}.csv'})
            return response
        else:
            raise HTTPException(status_code=response.status_code,
                                detail='Error from vite network')
    except Exception as e:
        raise e


@router.get('/order/{viteAddress}', description='These are the profits that you get when you do market making, which means when someone places buy and/or sell orders and fills the order book.')
async def load_market_making_data(viteAddress: str):
    try:
        api_url = get_dex_api_url(1) + '/mining/order/address'
        params = {'address': viteAddress}
        response = requests.get(url=api_url, params=params)

        if response.status_code == status.HTTP_200_OK:
            resp = response.json()

            check_response(resp)

            csv_data = []
            for entry in resp['data']['miningList']:
                dtobj = datetime.fromtimestamp(entry['date'], timezone.utc)

                dataRow = {
                    'miningAmount': entry['miningAmount'],
                    'miningRatio': entry['miningRatio'],
                    'cycleKey': entry['cycleKey'],
                    'date': entry['date'],
                    'dt': dtobj.strftime('%d/%m/%Y %H:%M:%S.%f')[:-3],
                }

                csv_data.append(dataRow)

            generated_message = generate_return_file_msg(csv_data)
            response = StreamingResponse(content=generated_message['file'],
                                         media_type='text/csv',
                                         headers={'Content-Disposition': 'filename=orderMining_{viteAddress}.csv'})
            return response
        else:
            raise HTTPException(status_code=response.status_code,
                                detail='Error from vite network')
    except Exception as e:
        raise e


@router.get('/pledge/{viteAddress}', description='Indicates the earnings in VX that are obtained when staked VITE on vitex.')
async def load_mining_pledge_data(viteAddress: str):
    try:
        api_url = get_dex_api_url(1) + '/mining/pledge'
        params = {'address': viteAddress}
        response = requests.get(url=api_url, params=params)

        if response.status_code == status.HTTP_200_OK:
            resp = response.json()

            check_response(resp)

            csv_data = []
            for staking in resp['data']['miningList']:
                dtobj = datetime.fromtimestamp(staking['date'], timezone.utc)

                dataRow = {
                    'pledgeAmount': staking['pledgeAmount'],
                    'miningAmount': staking['miningAmount'],
                    'miningToken': staking['miningToken'],
                    'status': staking['status'],
                    'date': staking['date'],
                    'dt': dtobj.strftime('%d/%m/%Y %H:%M:%S.%f')[:-3],
                }

                csv_data.append(dataRow)

            generated_message = generate_return_file_msg(csv_data)
            response = StreamingResponse(content=generated_message['file'],
                                         media_type='text/csv',
                                         headers={'Content-Disposition': 'filename=pledgeMining_{viteAddress}.csv'})
            return response
        else:
            raise HTTPException(status_code=response.status_code,
                                detail='Error from vite network')
    except Exception as e:
        raise e


def build_mining_data_list(miningList):
    data = []
    for entry in miningList:
        dtobj = datetime.fromtimestamp(entry['date'], timezone.utc)

        data_row = {
            'feeAmount': entry['feeAmount'],
            'miningAmount': entry['miningAmount'],
            'miningToken': entry['miningToken'],
            'status': entry['status'],
            'date': entry['date'],
            'dt': dtobj.strftime('%d/%m/%Y %H:%M:%S.%f')[:-3],
        }

        data.append(data_row)
    return data


def check_response(response):
    if (response['code'] != 0):
        raise HTTPException(status_code=500, detail=response['msg'])
    if not 'miningList' in response['data'] or len(response['data']['miningList']) == 0:
        raise HTTPException(
            status_code=404, detail='No data received from exchange')
