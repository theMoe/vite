from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import get_token_header, get_dex_api_url
import requests

router = APIRouter(
    prefix="/markets",
    tags=["markets"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get('/', description='Return a list of TradePairs e.g. VITE_USDT-000, tradeTokens e.g. VITE and quoteTokens e.g. VITE. Quote tokens are the tokens that are traded for.')
async def load_markets():
    try:
        api_url = get_dex_api_url(2) + '/markets'
        response = requests.get(url=api_url)

        if response.status_code == status.HTTP_200_OK:
            resp = response.json()

            if (resp['code'] != 0):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=resp['msg'])
            if not 'data' in resp or len(resp['data']) == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail='No data received from exchange')

            trade_pairs = []
            trade_tokens = []
            quote_tokens = []

            for tradePair in resp['data']:
                trade_pairs.append(tradePair['symbol'])

                if tradePair['tradeTokenSymbol'] not in trade_tokens:
                    trade_tokens.append(tradePair['tradeTokenSymbol'])

                if tradePair['quoteTokenSymbol'] not in quote_tokens:
                    quote_tokens.append(tradePair['quoteTokenSymbol'])

            data = {
                'tradePairs': trade_pairs,
                'tradeTokens': trade_tokens,
                'quoteTokens': quote_tokens,
            }

            return data
    except Exception as e:
        raise e
