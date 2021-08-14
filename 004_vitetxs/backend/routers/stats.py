from routers.tokens import get_token_info_list
from routers.sbp import get_sbp
from routers.prices import load_exchangerate
from database.repositories.fullnoderepository import get_active_node_count
from database.models import SessionLocal, get_db
from database.repositories.transactionsrepository import get_disctinct_accounts_by_transaction, get_last_transaction, get_transaction_count_since_last_day
from fastapi import APIRouter, Depends
from dependencies import get_token_header
from routers.net import load_syncInfo
from nodeFunctions import get_node_ip
from datetime import datetime, time

router = APIRouter(
    prefix="/stats",
    tags=["stats"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get('/', description='Returns a summary of stats')
async def get_all_stats(db: SessionLocal = Depends(get_db)):
    ip = get_node_ip()
    sync_info = await load_syncInfo(ip)

    block_height = sync_info['result']['current']
    transaction_count = await get_transaction_count_since_last_day(db)
    active_node_count = await get_active_node_count(db)
    total_accounts = await get_disctinct_accounts_by_transaction(db)
    total_super_nodes = len(await get_sbp(ip, False))
    token_list = await get_token_info_list(ip)
    total_tokens = len(token_list)
    for token in token_list:
        # VITE
        if token['tokenId'] == 'tti_5649544520544f4b454e6e40':
            token_supply = token['totalSupply']
            break
    exchange_rate = await load_exchangerate('VITE')
    usdt_price = exchange_rate['usdRate']

    response = {
        'block_height': block_height,
        'transactions_last_day': transaction_count,
        'super_nodes': total_super_nodes,
        'online_nodes': active_node_count,
        'tokens': total_tokens,
        'price': usdt_price,
        'total_supply': token_supply,
        'total_accounts': total_accounts
    }
    return response