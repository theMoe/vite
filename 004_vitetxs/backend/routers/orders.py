from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from starlette import status
from dependencies import get_token_header, get_dex_api_url
from datetime import datetime, timezone, date
from file_generating_service import generate_return_file_msg
from typing import Optional
import requests

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get('/{viteAddress}', description='Returns set orders on vitex')
async def load_orders(viteAddress: str, fromDate: Optional[date] = None, toDate: Optional[date] = None, sellBuy: Optional[int] = None, tradePair: Optional[str] = None, quoteToken: Optional[str] = None, tradeToken: Optional[str] = None, orderStatus: Optional[str] = None):
    api_url = get_dex_api_url(2) + '/orders'
    limit = 100

    dict_order_type = {
        0: 'Limit Order',
        1: 'Market Order',
    }

    dict_order_status = {
        0: 'Unkown',
        1: 'Pending',
        2: 'Received',
        3: 'Open',
        4: 'Filled',
        5: 'Partially Filled',
        6: 'Pending Cancel',
        7: 'Cancelled',
        8: 'Partially',
        9: 'Failed',
        10: 'Expired',
    }

    dict_side = {
        0: 'Buy Order',
        1: 'Sell Order',
    }

    params = {
        'address': viteAddress,
        'limit': limit,
    }

    if fromDate is not None:
        params['startTime'] = int(datetime(fromDate.year, fromDate.month, fromDate.day).timestamp())
    if toDate is not None:
        params['endTime'] = int(datetime(toDate.year, toDate.month, toDate.day).timestamp())
    params['side'] = sellBuy
    params['symbol'] = tradePair
    params['quoteTokenSymbol'] = quoteToken
    params['tradeTokenSymbol'] = tradeToken
    params['status'] = orderStatus

    filtered_params = {k: v for k, v in params.items() if v is not None}

    try:
        orders = []
        run_request = True
        while (run_request == True):
            print(filtered_params)
            response = requests.get(url=api_url, params=filtered_params)
            print(response.json())
            if response.status_code == status.HTTP_200_OK:
                resp = response.json()

                if (resp['code'] != 0):
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=resp['msg'])
                if not 'order' in resp['data'] or len(resp['data']['order']) == 0:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail='No data received from exchange')

                for order in resp['data']['order']:

                    dtobj = datetime.fromtimestamp(
                        order['createTime'], timezone.utc)

                    order_dict = {
                        'address': order['address'],
                        'orderId': order['orderId'],
                        'symbol': order['symbol'],
                        'tradeTokenSymbol': order['tradeTokenSymbol'],
                        'quoteTokenSymbol': order['quoteTokenSymbol'],
                        'side': dict_side[order['side']],
                        'price': order['price'],
                        'quantity': order['quantity'],
                        'amount': order['amount'],
                        'executedQuantity': order['executedQuantity'],
                        'executedAmount': order['executedAmount'],
                        'executedPercent': order['executedPercent'],
                        'executedAvgPrice': order['executedAvgPrice'],
                        'fee': order['fee'],
                        'status': dict_order_status[order['status']],
                        'type': dict_order_type[order['type']],
                        'createTime': order['createTime'],
                        'dt': dtobj.strftime('%d/%m/%Y %H:%M:%S.%f')[:-3]
                    }
                    orders.append(order_dict)

                if limit == len(resp['data']['order']):
                    last_order = resp['data']['order'][-1:]

                    filtered_params['endTime'] = last_order[0]['createTime'] - 1
                else:
                    run_request = False
            else:
                raise HTTPException(status_code=response.status_code,
                                    detail='Error from vite network')
        generated_message = generate_return_file_msg(orders)
        response = StreamingResponse(content=generated_message['file'],
                                     media_type='text/csv',
                                     headers={'Content-Disposition': 'filename=orders_{viteAddress}.csv'})
        return response

    except Exception as e:
        raise e
