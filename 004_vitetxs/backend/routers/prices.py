from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from dependencies import get_token_header, get_dex_api_url
from datetime import datetime, timezone, date
from file_generating_service import generate_return_file_msg
from typing import Optional
import requests

router = APIRouter(
    prefix="/prices",
    tags=["prices"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get('/', description='Get historical prices for provided pair')
async def load_prices(tradePair: str, interval: str, fromDate: Optional[date] = None, toDate: Optional[date] = None):
    # https://vite.wiki/dex/api/dex-apis.html#get-klines-candlestick-bars
    apiURL = get_dex_api_url(2) + '/klines'
    limit = 500

    params = {
        'symbol': tradePair,
        'interval': interval,
        'limit': limit,
    }

    if fromDate is not None:
        params['startTime'] = int(datetime(fromDate.year, fromDate.month, fromDate.day).timestamp())
    if toDate is not None:
        params['endTime'] = int(datetime(toDate.year, toDate.month, toDate.day).timestamp())

    filtered_params = {k: v for k, v in params.items() if v is not None}

    try:
        response = requests.get(url=apiURL, params=filtered_params)
        print(response.json())
        if response.status_code == 200:
            resp = response.json()
            prices = []
            if (resp['code'] != 0):
                raise HTTPException(status_code=500, detail=resp['msg'])
            if not ('t' in resp['data'] and
                    'c' in resp['data'] and
                    'p' in resp['data'] and
                    'h' in resp['data'] and
                    'l' in resp['data'] and
                    'v' in resp['data']):
                raise HTTPException(
                    status_code=404, detail='No data received from exchange')

            result_count = len(resp['data']['t'])

            for i in range(0, result_count):
                dtobj = datetime.fromtimestamp(
                    resp['data']['t'][i], timezone.utc)

                if (resp['data']['c'][i] != 0.0 and
                    resp['data']['p'][i] != 0.0 and
                        resp['data']['v'][i] != 0.0):
                    priceDict = {
                        'timeStamp': resp['data']['t'][i],
                        'dt': dtobj.strftime('%d/%m/%Y %H:%M'),
                        'symbol': tradePair,
                        'interval': interval,
                        'openPrice': resp['data']['p'][i],
                        'closePrice': resp['data']['c'][i],
                        'lowestPrice': resp['data']['l'][i],
                        'highestPrice': resp['data']['h'][i],
                        'tradeVolume': resp['data']['v'][i],
                    }

                    prices.append(priceDict)
        else:
            raise HTTPException(status_code=response.status_code,
                                detail='Error from vite network')

        generated_message = generate_return_file_msg(prices)
        response = StreamingResponse(content=generated_message['file'],
                                     media_type='text/csv',
                                     headers={'Content-Disposition': 'filename=prices.csv'})
        return response
    except Exception as e:
        raise e

@router.get('/exchangerate/{symbol}', description='Exchange rate for symbol')
async def load_exchangerate(symbol: str):

    try:
        response = requests.get(
                    f'https://api.vitex.net/api/v2/exchange-rate?tokenSymbols={symbol}')

        if response.status_code == 200:
            resp = response.json()

            if resp['code'] != 0:
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                                    detail='No data received')
            
            return resp['data'][0]

        else:
            raise HTTPException(status_code=response.status_code,
                                detail='Error from vite network')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)