from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from dependencies import get_token_header, get_dex_api_url
from datetime import datetime, timezone
from file_generating_service import generate_return_file_msg
import requests

router = APIRouter(
    prefix="/dividends",
    tags=["dividends"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get('/{viteAddress}', description='Determines the dividends a VITE address receives for staking VX on ViteX. Dividends are ETH, BTC and USDT')
async def load_dividends(viteAddress: str):
    api_url = get_dex_api_url(1) + '/dividend'

    try:
        params = {'address': viteAddress}
        response = requests.get(url=api_url, params=params)

        if response.status_code == status.HTTP_200_OK:
            resp = response.json()
            if (resp['code'] != 0):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=resp['msg'])
            if not 'dividendList' in resp['data'] or len(resp['data']['dividendList']) == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail='No data received from exchange')

            dividends = []
            for dividend in resp['data']['dividendList']:
                dtobj = datetime.fromtimestamp(dividend['date'], timezone.utc)

                dividend_dict = {'vxQuantity': dividend['vxQuantity']}

                if ('BTC' in dividend['dividendStat']):
                    dividend_dict[dividend['dividendStat']['BTC']['tokenDividends'][0]['tokenSymbol']
                                  ] = dividend['dividendStat']['BTC']['tokenDividends'][0]['amount']

                if ('ETH' in dividend['dividendStat']):
                    dividend_dict[dividend['dividendStat']['ETH']['tokenDividends'][0]['tokenSymbol']
                                  ] = dividend['dividendStat']['ETH']['tokenDividends'][0]['amount']

                if ('USDT' in dividend['dividendStat']):
                    dividend_dict[dividend['dividendStat']['USDT']['tokenDividends'][0]['tokenSymbol']
                                  ] = dividend['dividendStat']['USDT']['tokenDividends'][0]['amount']

                dividend_dict['date'] = dividend['date']
                dividend_dict['dt'] = dtobj.strftime(
                    '%d/%m/%Y %H:%M:%S.%f')[:-3]

                dividends.append(dividend_dict)

            generated_message = generate_return_file_msg(dividends)
            response = StreamingResponse(content=generated_message['file'],
                                         media_type='text/csv',
                                         headers={'Content-Disposition': 'filename=dividends_{viteAddress}.csv'})
            return response

        else:
            raise HTTPException(status_code=response.status_code,
                                detail='Error from vite network')
    except Exception as e:
        print(e)
        raise e
