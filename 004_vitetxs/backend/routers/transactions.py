from starlette.status import HTTP_200_OK
from database.repositories.transactionsrepository import create_transaction, get_all_transactions
from database.models import SessionLocal, get_db
from database.models.transactionmodel import DBTransaction, Transaction
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.params import Body
from fastapi.responses import StreamingResponse
from dependencies import get_token_header
from datetime import datetime, timedelta, timezone, date
from file_generating_service import generate_return_file_msg
from typing import Optional, List
from nodeFunctions import get_node_ip, get_url, get_header
import requests
import base64

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get('/', status_code=HTTP_200_OK)
async def fetch_all_transactions(limit: Optional[int] = 5000, db: SessionLocal = Depends(get_db)):
    return await get_all_transactions(limit, db)

@router.post('/store/', status_code=status.HTTP_200_OK)
async def consume_transaction_data(transaction: Transaction = Body(...), db: SessionLocal = Depends(get_db)):
    db_transaction = DBTransaction()
    db_transaction.block_type = transaction.block_type
    db_transaction.block_type_description = transaction.block_type_description
    db_transaction.account_block_height = transaction.account_block_height
    db_transaction.hash = transaction.hash
    db_transaction.account_address = transaction.account_address
    db_transaction.sbp_producer = transaction.sbp_producer
    db_transaction.from_address = transaction.from_address
    db_transaction.to_address = transaction.to_address
    db_transaction.amount = transaction.amount
    db_transaction.fee = transaction.fee
    db_transaction.data = transaction.data
    db_transaction.token_name = transaction.token_name
    db_transaction.token_symbol = transaction.token_symbol
    db_transaction.decimals = transaction.decimals
    db_transaction.token_id = transaction.token_id
    db_transaction.index = transaction.index
    db_transaction.first_snapshot_hash = transaction.first_snapshot_hash
    db_transaction.first_snapshot_height = transaction.first_snapshot_height
    db_transaction.timestamp = transaction.timestamp
    foo = await create_transaction(db, db_transaction)
    return foo

@router.get('/accountblock/{hash}', description='Returns transaction for a hash.')
async def load_transaction(hash: str):
    node_ip = get_node_ip()
    if node_ip == False:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail='No nodes available.')

    url = get_url(node_ip)
    header = get_header()
    body = {"jsonrpc": "2.0", "id": 2, "method": "ledger_getAccountBlockByHash", "params": [hash]}

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

@router.get('/{viteAddress}', description='Returns transactions for a VITE address that happened in the wallet.')
async def load_transactions(viteAddress: str, fromDate: Optional[date] = None, toDate: Optional[date] = None, viteAddressSender: Optional[List[str]] = Query(None)):
    node_ip = get_node_ip()
    if node_ip == False:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail='No nodes available.')

    filter_token = []  # ['VITE', 'BAN']

    url = get_url(node_ip)
    header = get_header()

    initial_page = 0
    end_page = True
    transactions = []
    transactions_per_request = 1000
    page_max = 2

    if (fromDate != None and toDate != None):
        toDate_plus_1 = toDate + timedelta(1)
    else:
        toDate_plus_1 = None
    print(viteAddressSender)
    while initial_page < page_max and end_page:
        body = get_body(viteAddress, initial_page, transactions_per_request)
        try:
            response = requests.post(url=url, json=body, headers=header)
            if response.status_code == status.HTTP_200_OK:
                resp = response.json()
                #print(resp)
                if resp['result'] == None:
                    print('Last requested page has no transaction results.')
                    end_page = False
                    break
                for result in resp['result']:
                    if result['tokenInfo'] is not None and result['tokenInfo']['tokenSymbol'] not in filter_token:
                        if (fromDate == None and toDate_plus_1 == None) or (fromDate <= date.fromtimestamp(result['timestamp']) and date.fromtimestamp(result['timestamp']) < toDate_plus_1):
                            if (viteAddressSender is None) or (viteAddressSender is not None and result['fromAddress'] in viteAddressSender):
                                toAddress = result['toAddress']
                                if toAddress == viteAddress:
                                    transaction_type = 'Recieved'
                                    transaction_multiplier = 1
                                else:
                                    transaction_type = 'Sent'
                                    transaction_multiplier = -1

                                amount = int(result['amount'])
                                decimals = int(result['tokenInfo']['decimals'])
                                decimal_amount = (
                                    amount / 10**decimals) * transaction_multiplier

                                memo = None
                                if result['data'] is not None:
                                    memo_base64 = str(result['data'])
                                    memo = base64.b64decode(memo_base64).decode('utf-8',errors='ignore')
                                dtobj = datetime.fromtimestamp(
                                    result['timestamp'], timezone.utc)

                                transaction = {
                                    'fromAddress': result['fromAddress'],
                                    'toAddress': toAddress,
                                    'transactionType': transaction_type,
                                    'decimalAmount': decimal_amount,
                                    'amount': str(amount),
                                    'decimals': decimals,
                                    'fee': result['fee'],
                                    'tokenName': result['tokenInfo']['tokenName'],
                                    'tokenSymbol': result['tokenInfo']['tokenSymbol'],
                                    'datetime': result['timestamp'],
                                    'dt': dtobj.strftime('%d/%m/%Y %H:%M:%S.%f')[:-3],
                                    'txHash': result['hash'],
                                    'memo': memo
                                }
                                transactions.append(transaction)
                        elif (fromDate > date.fromtimestamp(result['timestamp'])):
                            end_page = False
                            break
            else:
                print(response.status_code)
                end_page = False
                break
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail='Exception during request.')

        initial_page = initial_page + 1

    if len(transactions) > 0:
        generated_message = generate_return_file_msg(transactions)
        response = StreamingResponse(content=generated_message['file'],
                                     media_type='text/csv',
                                     headers={'Content-Disposition': 'filename=transactions_{viteAddress}.csv'})
        return response
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail='No transactions available')


def get_body(viteAddr, pg, transPerRequest):
    body = {
        'jsonrpc': '2.0',
        'id': 2,
        'method': 'ledger_getAccountBlocksByAddress',
        'params': [viteAddr, pg, transPerRequest]
    }
    return body
