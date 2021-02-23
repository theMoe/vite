from flask import Flask, Response, render_template, request, redirect
from io import StringIO
import pandas as pd
import requests
import json
import random
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

def getDexAPIURL(version):
    return "https://api.vitex.net/api/v" + str(version)

def loadDividends(viteAddress):
    apiURL = getDexAPIURL(1) + "/dividend"

    params = {
        'address': viteAddress,
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

def loadOrders(viteAddress):
    # https://vite.wiki/dex/api/dex-apis.html#get-orders
    apiURL = getDexAPIURL(2) + "/orders"

    params = {
        'address': viteAddress,
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

def loadPrice(): #pair, interval, limit, fromDate, toDate):
    apiURL = getDexAPIURL(2) + "/klines"

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
                        print("good ip " + result['ip'])
                        return result['ip']
                    else:
                        print("bad ip " + result['ip'])

    return False
# US, HK, HK
backupIP = ['170.106.33.134', '150.109.116.1', '150.109.51.8']

def getURL(ip):
    return 'http://' + ip + ':48132'

def getHeader():
    header = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/json"
    }
    return header

def getBody(viteAddr, pg, transPerRequest):
    body = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "ledger_getAccountBlocksByAddress",
        "params": [viteAddr, pg, transPerRequest]
    }
    return body

def requestNodeData(viteAddress, transactionsPerRequest, pageMax, filterTime):
    nodeIP = getNodeIP()
    if nodeIP == False:
        print('Connection ERROR...')
        # return [{'errorMsg': 'Connection error...'}]
        # sys.exit('  ###> You have to enter an IP of a VITE node.')

    nodeDetails = [
        {'name': '', 'IP': nodeIP}
    ]

    filterToken = [] # ['VITE', 'BAN']

    if len(nodeDetails) == 1:
        url = getURL(nodeDetails[0]['IP'])
        header = getHeader()

        page = 0
        endPage = True
        transactions = []
        print(url)
        while page < pageMax and endPage:
            body = getBody(viteAddress, page, transactionsPerRequest)
            try:
                response = requests.post(url=url, json=body, headers=header)
                #print("Resp Code: " + str(response.status_code))
                if response.status_code == 200:
                    resp = response.json()
                    #print(resp)
                    if resp['result'] == None:
                        print('Last requested page has no transaction results.')
                        endPage = False
                        break
                    for result in resp['result']:
                        if result['tokenInfo']['tokenSymbol'] not in filterToken:
                            if (filterTime[0] == None and filterTime[1] == None) or (int(filterTime[0]) <= result['timestamp'] and result['timestamp'] <= int(filterTime[1])):
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
                                    'dt': dtobj.strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
                                }

                                transactions.append(transaction)
                else:
                    print(response.status_code)
                    endPage = False
                    break
            except Exception as e:
                print(e)
                return [{'errorMsg': 'Exception during request.'}]
                # sys.exit('  ###> Exception during request.')

            page = page + 1
            print('Downloaded page ' + str(page))
   
        if len(transactions) > 0:
            return transactions

        print('Total transactions downloaded: ' + str(len(transactions)))
        print('Done')

errMsg = {'errShow': False, 'errMsg': ''}

def updateErr(show, msg):
    global errMsg
    errMsg['errShow'] = show
    errMsg['errMsg'] = msg

@app.route("/impressum")
def impressum():
    return render_template("impressum.html", viteTxsVersion = getVersion())

@app.route("/")
def index():
    global errMsg
    errShowLocal = errMsg['errShow']
    errMsgLocal = errMsg['errMsg']
    updateErr(False, '')
    if errShowLocal == False:
        return render_template("index.html", errShow = False, pageShow = False, viteTxsVersion = getVersion())
    else:
        return render_template("index.html", errShow = True, errMsg = errMsgLocal, pageShow = False, viteTxsVersion = getVersion())


@app.route("/", methods=["POST"]) #/<file_name>
def get_file(): #file_name
    global errMsg
    viteAddress = request.form.get("viteAddress")
    transactionsPerRequest = 1000 #0 # int(request.form.get("tpp"))
    pageMax = 100 # int(request.form.get("mP"))
    fromDate = request.form.get("fromDate")
    toDate = request.form.get("toDate")

    filterTime = [None, None]
    if fromDate != "":
        filterTime[0] = int(datetime.strptime(fromDate, '%Y-%m-%d').timestamp())
    if toDate != "":
        filterTime[1] = int((datetime.strptime(toDate, '%Y-%m-%d') + timedelta(days=1)).timestamp())

    if filterTime[0] != None and filterTime[1] != None:
        if filterTime[0] > filterTime[1]:
            updateErr(True, 'From date must be earlier then to date')
            return redirect("/")
    
    if (filterTime[0] == None and filterTime[1] != None) or (filterTime[0] != None and filterTime[1] == None):
        updateErr(True, 'Enter both dates or no dates at all')
        return redirect("/")

    if viteAddress != "":
        data = requestNodeData(viteAddress.strip(), transactionsPerRequest, pageMax, filterTime)
        if len(data) > 0:
            if 'errorMsg' in data[0]:
                updateErr(True, str(data[0]['errorMsg']))
                return redirect("/")
            else:
                data_df = pd.DataFrame(data)
                generated_file = generate_csv_file(data_df)
                response = Response(generated_file, mimetype="text/csv")
                # add a filename
                response.headers.set(
                    "Content-Disposition", "attachment", filename="{0}.csv".format(viteAddress)
                )
                
                return response
        else:
            updateErr(True, 'No Data')
            return redirect("/")
    else:
        updateErr(True, 'VITE address is required')
        return redirect("/")

def generate_csv_file(file_df):
    # Create an o/p buffer
    file_buffer = StringIO()

    # Write the dataframe to the buffer
    file_df.to_csv(file_buffer, encoding="utf-8", index=False, sep=",")

    # Seek to the beginning of the stream
    file_buffer.seek(0)
    return file_buffer

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')