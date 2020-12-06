import argparse
import requests
import json
import os
import sys
import pandas as pd         # pip install pandas / alternativ, if several python installations: python3 -m pip install pandas
from datetime import datetime, timezone

# Create the parser
parser = argparse.ArgumentParser(description='Request parameters')
# Add the arguments
parser.add_argument('--vaddr', type=str, help='VITE address')
parser.add_argument('--nodeIP', type=str, help='VITE node IP')
parser.add_argument('--fromDate', type=lambda s: datetime.strptime(s, '%Y-%m-%d'), help='From date YYYY-MM-DD (incl.)')
parser.add_argument('--toDate', type=lambda s: datetime.strptime(s, '%Y-%m-%d'), help='To date YYYY-MM-DD (incl.)')

# Execute the parse_args() method
args = parser.parse_args()

fromDate = args.fromDate
toDate = args.toDate
viteAddress = args.vaddr
nodeIP = args.nodeIP

if fromDate != None:
    fromDate = datetime.timestamp(fromDate)
if toDate != None:
    toDate = datetime.timestamp(toDate)

if fromDate != None and toDate != None:
    if toDate < fromDate:
        sys.exit('  ###> toDate must be equal or greater than fromDate')
    
filterToken = [] # ['VITE', 'BAN']
filterTime = [fromDate, toDate]

if nodeIP == None:
    sys.exit('  ###> You have to enter an IP of a VITE node.')

nodeDetails = [
    {'name': '', 'IP': nodeIP}
]
print(nodeDetails)
if viteAddress == None:
    sys.exit('  ###> You have to enter a VITE address with parameter --vaddr')

transactionsPerRequest = 300
pageMax = 20

path = os.path.dirname(os.path.abspath(__file__))
fileName = 'VITE_transactions.json'

def createCSV():
    fullPath = path + '/' + fileName
    if os.path.exists(fullPath):
        df = pd.read_json (fullPath)
        export_csv = df.to_csv (fullPath + '.csv', index = None, header=True)
        return True
    else:
        return False

def writeJSON(fileName, data):
    try:
        with open(path + '/' + fileName, 'w') as outfile:
            json.dump(data, outfile)
        return True
    except:
        return False

def loadJSON(fileName):
    fullPath = path + '/' + fileName
    if os.path.exists(fullPath):
        with open(path + '/' + fileName) as outfile:
            data = json.load(outfile)
            return data
    else:
        return None    

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

def requestNodeData():
    if len(nodeDetails) == 1:
        url = getURL(nodeDetails[0]['IP'])
        header = getHeader()

        page = 0
        endPage = True
        transactions = []

        while page < pageMax and endPage:
            body = getBody(viteAddress, page, transactionsPerRequest)
            try:
                response = requests.post(url=url, json=body, headers=header)
            
                if response.status_code == 200:
                    resp = response.json()
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
                                    'datetime': result['timestamp'] #, #dtobj,
                                    #'dt': dtobj.strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
                                }

                                transactions.append(transaction)
                else:
                    print(response.status_code)
                    endPage = False
                    break
            except:
                sys.exit('  ###> Exception during request.')

            page = page + 1
            print('Downloaded page ' + str(page))
   
        if len(transactions) > 0:
            statusJSON = writeJSON(fileName,transactions)
        
            if statusJSON:
                print('JSON created')
                statusCSV = createCSV()
            else:
                print('No JSON created')
            
            if statusCSV:
                print('CSV created')
            else:
                print('No CSV created')

        print('Total transactions downloaded: ' + str(len(transactions)))
        print('Done')

requestNodeData()

