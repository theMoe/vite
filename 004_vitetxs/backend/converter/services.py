from io import StringIO
import random
import requests
from datetime import datetime, timezone, timedelta
import pandas as pd


def __getDexAPIURL(version):
        return 'https://api.vitex.net/api/v' + str(version)

# https://api.vitex.net/api/v1/mining/order/invite?address=

# Referral
# https://api.vitex.net/api/v1/mining/invite?address=
def loadInviteMiningData(viteAddress):
    apiURL = __getDexAPIURL(1) + '/mining/invite'

    params = {
        'address': viteAddress,
    }

    data = []

    try:
        response = requests.get(url=apiURL, params=params)
        if response.status_code == 200:
            resp = response.json()
            #print(resp)

            if (resp['code'] != 0):
                return {'errorMsg': resp['msg']}
            if not 'data' in resp:
                return {'errorMsg': 'No data received from exchange'}
            if not 'miningList' in resp['data']:
                return {'errorMsg': 'No invite mining data received from exchange'}
            
            for entry in resp['data']['miningList']:
                dtobj = datetime.fromtimestamp(entry['date'], timezone.utc)
                
                dataRow = {
                    'feeAmount': entry['feeAmount'],
                    'miningAmount': entry['miningAmount'],
                    'miningToken': entry['miningToken'],
                    'status': entry['status'],
                    'date': entry['date'],
                    'dt': dtobj.strftime('%d/%m/%Y %H:%M:%S.%f')[:-3],
                }

                data.append(dataRow)

            return getReturnFileMsg(data, 'invite mining data')
        else:
            return {'errorMsg': response.status_code}
    except Exception as e:
        print (e)
        return {'errorMsg': 'Exception during request.'}

# Trading
# https://api.vitex.net/api/v1/mining/trade?address=
def loadTradingMiningData(viteAddress):
    apiURL = __getDexAPIURL(1) + '/mining/trade'

    params = {
        'address': viteAddress,
    }

    data = []

    try:
        response = requests.get(url=apiURL, params=params)
        if response.status_code == 200:
            resp = response.json()
            #print(resp)

            if (resp['code'] != 0):
                return {'errorMsg': resp['msg']}
            if not 'data' in resp:
                return {'errorMsg': 'No data received from exchange'}
            if not 'miningList' in resp['data']:
                return {'errorMsg': 'No trading mining data received from exchange'}
            
            for entry in resp['data']['miningList']:
                dtobj = datetime.fromtimestamp(entry['date'], timezone.utc)
                
                dataRow = {
                    'feeAmount': entry['feeAmount'],
                    'miningAmount': entry['miningAmount'],
                    'miningToken': entry['miningToken'],
                    'status': entry['status'],
                    'date': entry['date'],
                    'dt': dtobj.strftime('%d/%m/%Y %H:%M:%S.%f')[:-3],
                }

                data.append(dataRow)

            return getReturnFileMsg(data, 'trading mining data')
        else:
            return {'errorMsg': response.status_code}
    except Exception as e:
        print (e)
        return {'errorMsg': 'Exception during request.'}

# Market-Making
# https://api.vitex.net/api/v1/mining/order/address?address=
def loadMarketMakingData(viteAddress):
    apiURL = __getDexAPIURL(1) + '/mining/order/address'

    params = {
        'address': viteAddress,
    }

    data = []

    try:
        response = requests.get(url=apiURL, params=params)
        if response.status_code == 200:
            resp = response.json()
            #print(resp)

            if (resp['code'] != 0):
                return {'errorMsg': resp['msg']}
            if not 'data' in resp:
                return {'errorMsg': 'No data received from exchange'}
            if not 'miningList' in resp['data']:
                return {'errorMsg': 'No market-mining data received from exchange'}
            
            for entry in resp['data']['miningList']:
                dtobj = datetime.fromtimestamp(entry['date'], timezone.utc)
                
                dataRow = {
                    'miningAmount': entry['miningAmount'],
                    'miningRatio': entry['miningRatio'],
                    'cycleKey': entry['cycleKey'],
                    'date': entry['date'],
                    'dt': dtobj.strftime('%d/%m/%Y %H:%M:%S.%f')[:-3],
                }

                data.append(dataRow)

            return getReturnFileMsg(data, 'market-making data')
        else:
            return {'errorMsg': response.status_code}
    except Exception as e:
        print (e)
        return {'errorMsg': 'Exception during request.'}

# Staking
# https://api.vitex.net/api/v1/mining/pledge?address=
def loadStakingData(viteAddress):
    apiURL = __getDexAPIURL(1) + '/mining/pledge'

    params = {
        'address': viteAddress,
    }

    data = []

    try:
        response = requests.get(url=apiURL, params=params)
        if response.status_code == 200:
            resp = response.json()
            #print(resp)

            if (resp['code'] != 0):
                return {'errorMsg': resp['msg']}
            if not 'data' in resp:
                return {'errorMsg': 'No data received from exchange'}
            if not 'miningList' in resp['data']:
                return {'errorMsg': 'No dividends received from exchange'}
            
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

                data.append(dataRow)

            return getReturnFileMsg(data, 'stakings')
        else:
            return {'errorMsg': response.status_code}
    except Exception as e:
        print (e)
        return {'errorMsg': 'Exception during request.'}

def getReturnFileMsg(dictData, msg):
    if len(dictData) > 0:
        data_df = pd.DataFrame(dictData)
        generated_file = generate_csv_file(data_df)
        print('Total ' + msg + ' downloaded: ' + str(len(dictData)))
        print('Done')
        return {'file': generated_file, 'count': len(dictData)}
    else:
        return {'errorMsg': 'No ' + msg + ' available'}

def loadDividends(viteAddress):
    apiURL = __getDexAPIURL(1) + '/dividend'

    params = {
        'address': viteAddress,
    }

    dividends = []

    try:
        response = requests.get(url=apiURL, params=params)
        if response.status_code == 200:
            resp = response.json()
            #print(resp)

            if (resp['code'] != 0):
                return {'errorMsg': resp['msg']}
            if not 'data' in resp:
                return {'errorMsg': 'No data received from exchange'}
            if not 'dividendList' in resp['data']:
                return {'errorMsg': 'No dividends received from exchange'}
            
            for dividend in resp['data']['dividendList']:
                dtobj = datetime.fromtimestamp(dividend['date'], timezone.utc)
                
                dividendDict = {
                    'vxQuantity': dividend['vxQuantity'],
                }

                if ('BTC' in dividend['dividendStat']):
                    dividendDict[dividend['dividendStat']['BTC']['tokenDividends'][0]['tokenSymbol']] = dividend['dividendStat']['BTC']['tokenDividends'][0]['amount'] 

                if ('ETH' in dividend['dividendStat']):
                    dividendDict[dividend['dividendStat']['ETH']['tokenDividends'][0]['tokenSymbol']] = dividend['dividendStat']['ETH']['tokenDividends'][0]['amount'] 

                if ('USDT' in dividend['dividendStat']):
                    dividendDict[dividend['dividendStat']['USDT']['tokenDividends'][0]['tokenSymbol']] = dividend['dividendStat']['USDT']['tokenDividends'][0]['amount'] 

                dividendDict['date'] = dividend['date']
                dividendDict['dt'] = dtobj.strftime('%d/%m/%Y %H:%M:%S.%f')[:-3]

                dividends.append(dividendDict)

            if len(dividends) > 0:
                data_df = pd.DataFrame(dividends)
                generated_file = generate_csv_file(data_df)
                print('Total dividends downloaded: ' + str(len(dividends)))
                print('Done')
                return {'file': generated_file, 'dividendsCount': len(dividends)}
            else:
                return {'errorMsg': 'No dividends available'}
        else:
            return {'errorMsg': response.status_code}
    except Exception as e:
        print (e)
        return {'errorMsg': 'Exception during request.'}

def loadOrders(viteAddress, limit, filterTime, sellBuy):
    # https://vite.wiki/dex/api/dex-apis.html#get-orders
    apiURL = __getDexAPIURL(2) + '/orders'
    # Name	            Type	Is Required?	Description
    # address	        STRING	YES	            User's account address (not delegation address)
    # symbol	        STRING	NO	            Trading pair name. For example, GRIN-000_BTC-000
    # quoteTokenSymbol	STRING	NO	            Quote token symbol. For example, BTC-000
    # tradeTokenSymbol	STRING	NO	            Trade token symbol. For example, GRIN-000
    # startTime	        LONG	NO	            Start time (s)
    # endTime	        LONG	NO            	End time (s)
    # side	            INTEGER	NO            	Order side. 0 - buy, 1 - sell
    # status	        INTEGER	NO            	Order status, valid in [ 0-10 ]. 3 , 5 - returns orders that are unfilled or partially filled; 7 , 8 - returns orders that are cancelled or partially cancelled
    # offset	        INTEGER	NO            	Search starting index, starts at 0 , default 0
    # limit	            INTEGER	NO            	Search limit, default 30 , max 100
    # total	            INTEGER	NO          	Include total number searched in result? 0 - not included, 1 - included. Default is 0 , in this case total=-1 in response

    # Order Type
    # Code	Status	        Description
    # 0	    Limit Order	    Limit Order
    # 1	    Market Order	Market Order (not supported at present)
    dictOrderType = {
        0: 'Limit Order',
        1: 'Market Order',
    }
    # Order Status
    # Code	Status	            Description
    # 0	    Unknown	            Status unknown
    # 1	    Pending             Request	Order submitted. A corresponding request transaction has been created on the blockchain
    # 2	    Received            Order received by ViteX smart contract. Not yet dispatched into matching engine
    # 3	    Open	            Order unfilled
    # 4	    Filled	            Order completely filled
    # 5	    Partially Filled	Order partially filled
    # 6	    Pending Cancel  	Cancel order request submitted. A corresponding request transaction has been created on the blockchain
    # 7	    Cancelled	        Order cancelled
    # 8	    Partially           Cancelled	Order partially cancelled (order is partially filled and then cancelled)
    # 9	    Failed	            Order failed
    # 10  	Expired	            Order expired
    dictOrderStatus = {
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
    # Side
    # Code	Status	    Description
    # 0	    Buy Order	Buy
    # 1	    Sell Order	Sell
    dictSide = {
        0: 'Buy Order',
        1: 'Sell Order',
    }

    params = {
        'address': viteAddress,
        'limit': limit,
    }

    if (filterTime[0] != None and filterTime[1] != None):
        params['startTime'] = filterTime[0]
        params['endTime'] = filterTime[1]
    
    if (sellBuy != None):
        params['side'] = sellBuy
    
    #if (orderStatus != None):
    #    params['status'] = orderStatus
    
    orders = []

    try:
        response = requests.get(url=apiURL, params=params)
        if response.status_code == 200:
            resp = response.json()
            #print(resp)
            if (resp['code'] != 0):
                return {'errorMsg': resp['msg']}
            if not 'data' in resp:
                return {'errorMsg': 'No data received from exchange'}
            if not 'order' in resp['data']:
                return {'errorMsg': 'No orders received from exchange'}
            
            for order in resp['data']['order']:
                
                dtobj = datetime.fromtimestamp(order['createTime'], timezone.utc)
                
                orderDict = {
                    'address': order['address'],                    # 'vite_b2d3a3fe5e5ec11ad8c6823843482c2000920e2ef96d417e85', 
                    'orderId': order['orderId'],                    # '6d15d8b082ae77d88bb28efcbe8002fd501da323ccac30b2a465d48fbe108a52', 
                    'symbol': order['symbol'],                      # 'VITE_ETH-000', 
                    'tradeTokenSymbol': order['tradeTokenSymbol'],  # 'VITE', 
                    'quoteTokenSymbol': order['quoteTokenSymbol'],  # 'ETH-000', 
                    #'tradeToken': 'tti_5649544520544f4b454e6e40', 
                    #'quoteToken': 'tti_687d8a93915393b219212c73', 
                    'side': dictSide[order['side']],                # 1, 
                    'price': order['price'],                        # '0.0000255', 
                    'quantity': order['quantity'],                  # '2500.0', 
                    'amount': order['amount'],                      # '0.0637500', 
                    'executedQuantity': order['executedQuantity'],  # '0.0', 
                    'executedAmount': order['executedAmount'],      # '0.0000000', 
                    'executedPercent': order['executedPercent'],    # '0.0000000', 
                    'executedAvgPrice': order['executedAvgPrice'],  # '0.0000000',
                    'fee': order['fee'],                            # '0.0000000', 
                    'status': dictOrderStatus[order['status']],     #  3, 
                    'type': dictOrderType[order['type']],           # 0, 
                    'createTime': order['createTime'],              #  1613169379
                    'dt': dtobj.strftime('%d/%m/%Y %H:%M:%S.%f')[:-3]
                }
                orders.append(orderDict)

            if len(orders) > 0:
                data_df = pd.DataFrame(orders)
                generated_file = generate_csv_file(data_df)
                print('Total orders downloaded: ' + str(len(orders)))
                print('Done')
                return {'file': generated_file, 'ordersCount': len(orders)}
            else:
                return {'errorMsg': 'No orders available'}
        else:
            return {'errorMsg': response.status_code}
    except Exception as e:
        print (e)
        return {'errorMsg': 'Exception during request.'}

def loadPrice(): #pair, interval, limit, fromDate, toDate):
    apiURL = __getDexAPIURL(2) + '/klines'

    params = {
        'symbol': 'VITE_USDT-000',
        'interval': 'day',
        'limit': 10,
        'startTime': 1577836800,
        'endTime': 1609459200
    }

    try:
        response = requests.get(url=apiURL, params=params)
        if response.status_code == 200:
            resp = response.json()
            print(resp)
            return True
        else:
            return False
    except:
        return False

def getVersion():
    return 'v0.04'

def tryIP(ip):
    url = getURL(ip)
    header = getHeader()
    body = {
        'jsonrpc': '2.0',
        'id': 2,
        'method': 'ledger_getSnapshotChainHeight',
        'params': None
    }
    try:
        response = requests.post(url=url, json=body, headers=header, timeout=2)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def peers(ip):
    url = getURL(ip)
    header = getHeader()
    body = {
        'jsonrpc': '2.0',
        'id': 3,
        'method': 'net_nodeInfo',
        'params': None
    }
    try:
        response = requests.post(url=url, json=body, headers=header, timeout=2)
        if response.status_code == 200:
            resp = response.json()
            print(resp)
            return True
        else:
            return False
    except:
        return False

def getNodeIP():
    global backupIP
    localIP = backupIP.copy()
    random.shuffle(localIP)
    for ip in localIP:
        if tryIP(ip) == True:
            print('good backIP ' + ip)
            return ip
        else:
            print('bad backIP ' + ip)
    
    urlReward = 'https://rewardapi.vite.net/reward/full/real?cycle='
    cycle_incomplete =  int((datetime.timestamp(datetime.now()) - 1558411200) / 24 / 3600)
    url = urlReward + str(cycle_incomplete)
    response = requests.get(url=url)

    if response.status_code == 200:
        resp = response.json()
        if resp['msg'] == 'success':
            for result in resp['data']:
                if result['onlineRatio'] == 1.0:
                    if tryIP(result['ip']) == True:
                        print('good ip ' + result['ip'])
                        return result['ip']
                    else:
                        print('bad ip ' + result['ip'])

    return False
# US, HK, HK
backupIP = ['170.106.33.134', '150.109.116.1', '150.109.51.8']

def getURL(ip):
    return 'http://' + ip + ':48132'

def getHeader():
    header = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json'
    }
    return header

def getBody(viteAddr, pg, transPerRequest):
    body = {
        'jsonrpc': '2.0',
        'id': 2,
        'method': 'ledger_getAccountBlocksByAddress',
        'params': [viteAddr, pg, transPerRequest]
    }
    return body

def requestNodeData(viteAddress, transactionsPerRequest, pageMax, filterTime):
    nodeIP = getNodeIP()
    if nodeIP == False:
        print('Connection ERROR...')
        return {'errorMsg': 'Connection error...'}
    
    filterToken = [] # ['VITE', 'BAN']

    url = getURL(nodeIP)
    header = getHeader()

    page = 0
    endPage = True
    transactions = []
    
    print(url)
    while page < pageMax and endPage:
        body = getBody(viteAddress, page, transactionsPerRequest)
        try:
            # req = urllib.request.Request(url)
            # req.add_header('Content-Type', 'application/json; charset=utf-8')
            # jsonBody = json.dumps(body)
            # jsonBytes = jsonBody.encode('utf-8')
            # req.add_header('Content-Length', len(jsonBytes))
            # response = urllib.request.urlopen(req, jsonBytes)
            # print(json.load(response))

            # req = urllib.request.Request(url, jsonBytes, header)
            # response = urllib.request.urlopen(req)
            # jsonRead = json.load(response)
            # print(jsonRead)
            response = requests.post(url=url, json=body, headers=header)
            if response.status_code == 200:
                resp = response.json()
                #print(resp)
                if resp['result'] == None:
                    print('Last requested page has no transaction results.')
                    endPage = False
                    break
                for result in resp['result']:
                    if result['tokenInfo'] is not None:
                        if result['tokenInfo']['tokenSymbol'] not in filterToken:
                            if (filterTime[0] == None and filterTime[1] == None) or (filterTime[0] <= result['timestamp'] and result['timestamp'] <= filterTime[1]):
                                toAddress = result['toAddress']
                                if toAddress == viteAddress:
                                    transactionType = 'Recieved'
                                    transactionMultiplier = 1
                                else:
                                    transactionType = 'Sent'
                                    transactionMultiplier = -1

                                amount = int(result['amount'])
                                decimals = int(result['tokenInfo']['decimals'])
                                decimalAmount = (amount / 10**decimals) * transactionMultiplier

                                dtobj = datetime.fromtimestamp(result['timestamp'], timezone.utc) 

                                transaction = {
                                    'fromAddress': result['fromAddress'],
                                    'toAddress': toAddress,
                                    'transactionType': transactionType,
                                    'decimalAmount': decimalAmount,
                                    'amount': str(amount),
                                    'decimals': decimals,
                                    'fee': result['fee'],
                                    'tokenName': result['tokenInfo']['tokenName'],
                                    'tokenSymbol': result['tokenInfo']['tokenSymbol'],
                                    'datetime': result['timestamp'], #, #dtobj,
                                    'dt': dtobj.strftime('%d/%m/%Y %H:%M:%S.%f')[:-3]
                                }
                                transactions.append(transaction)
                            elif (filterTime[0] > result['timestamp']):
                                print('Last requested page has older transactions then requested')
                                endPage = False
                                break
            else:
                print(response.status_code)
                endPage = False
                break
        except Exception as e:
            print(e)
            return {'errorMsg': 'Exception during request.'}

        page = page + 1
        print('Downloaded page ' + str(page))

    if len(transactions) > 0:
        data_df = pd.DataFrame(transactions) # generate_fake_data()
        generated_file = generate_csv_file(data_df)
        print('Total transactions downloaded: ' + str(len(transactions)))
        print('Done')
        return {'file': generated_file, 'transactionsCount': len(transactions)}
    else:
        return {'errorMsg': 'No transactions available'}

def getBody_getAccountInfoByAddress(viteAddress):
    body = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "ledger_getAccountInfoByAddress",
        "params": [viteAddress]
    }
    return body

def getAccountInfo(viteAddress):
    print('A')
    nodeIP = getNodeIP()
    if nodeIP == False:
        print('Connection ERROR...')
        return {'errorMsg': 'Connection ERROR...', 'status': 999}
    
    url = getURL(nodeIP)
    header = getHeader()
    body = getBody_getAccountInfoByAddress(viteAddress)
    print(url)
    try:
        response = requests.post(url=url, json=body, headers=header)
        if response.status_code == 200:
            resp = response.json()
            return resp
        else:
            print(response.status_code)
            return {'errorMsg': 'Error...', 'status': response.status_code}
    except Exception as e:
        print(e)
        return {'errorMsg': e, 'status': 999}

def getBody_getSBPVoteListe():
    body = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "contract_getSBPVoteList",
        "params": None
    }
    return body

def getSBP():
    nodeIP = getNodeIP()
    if nodeIP == False:
        print('Connection ERROR...')
        return {'errorMsg': 'Connection ERROR...', 'status': 999}
    
    url = getURL(nodeIP)
    header = getHeader()
    body = getBody_getSBPVoteListe()

    try:
        response = requests.post(url=url, json=body, headers=header)
        if response.status_code == 200:
            resp = response.json()
            return resp
        else:
            return {'errorMsg': 'Error...', 'status': response.status_code}
    except Exception as e:
        print(e)
        return {'errorMsg': e, 'status': 999}

def generate_csv_file(file_df):
    # Create an o/p buffer
    file_buffer = StringIO()

    # Write the dataframe to the buffer
    file_df.to_csv(file_buffer, encoding='utf-8', index=False, sep=',')

    # Seek to the beginning of the stream
    file_buffer.seek(0)
    return file_buffer
