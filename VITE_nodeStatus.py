import requests
import json
import os
from datetime import datetime

#now = datetime.now()
#print("now =", now)
# # dd/mm/YY H:M:S
#dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#print("date and time =", dt_string)	

# urlGetAlivePeers = 'https://stats.vite.net/api/getAlivePeers?address='
nodeDetails = [
    {'name': '####', 'IP': '##.##.##.##'},
    {'name': '####', 'IP': '##.##.##.##'}
]
path = os.path.dirname(os.path.abspath(__file__))
fileName = 'VITE_Data.json'

# Create telgram bot
# a) Open Telegram
# b) Open new conversation with @BotFather
# c) Create new bot sending to @BotFather this text: /newbot
# d) Answer to @BotFather with a name of your bot (ES: botname)
# e) Answer to @BotFather with a username of your bot (ES: botname_bot)
# f) Copy the HTTP API that @BotFather has create to a text note.
# g) Create a group on your Telegram and add your new bot to the group.
# h) Add @my_id_bot to the same group.
# i) Send /getgroupid to the group and copy the Group ID to a text note.
def telegramMsg(msg):
    data = {
        'chat_id': '###GROUP ID###',
        'text': msg,
        'user': '###',
        'password': '###',
        'to': '###'
    }
    url = 'https://api.telegram.org/bot[###BOT API###]/sendMessage'
    response = requests.post(url, data=data)
    #print(response.status_code)

def prepareMsg(data):
    msg = 'VITE-Nodes Update:'
    send = False
    for node in data:
        msg = msg + '\n'
        msg = msg + node['node'] + ":"
        first = True
        for result in node['results']:
            if first == False:
                msg = msg + ' ('
            else:
                msg = msg + ' '
            
            if result['status'] == True:
                height = int(result['result']['result'])
                msg = msg + '{:,}'.format(height).replace(',','.')
            else:
                send = True
                msg = msg + ' ' + node['result']

            if first == False:
                msg = msg + ')'
            first = False
    print(msg)
    if send == True:
        telegramMsg(msg)

def writeJSON(fileName, data):
    with open(path + '/' + fileName, 'w') as outfile:
                    json.dump(data, outfile)

def loadJSON(fileName):
    fullPath = path + '/' + fileName
    if os.path.exists(fullPath):
        #print('yes')
        with open(path + '/' + fileName) as outfile:
            data = json.load(outfile)
            return data
    else:
        return None    

def getURL(ip):
    return 'http://' + ip + ':48132'

def getLastLocalData(localData, nodeName):
    if localData == None:
        return None
    for data in localData:
        if data['node'] == nodeName:
            if len(data['results']) < 0:
                return None
            else:
                return data['results'][0]
    return None

def requestNodeData():
    localData = loadJSON(fileName)
    if len(nodeDetails) > 0:
        respData = []
        for node in nodeDetails:
            url = getURL(node['IP'])
            header = {
                'Cache-Control': 'no-cache',
                'Content-Type': 'application/json'
            }
            body = {
                'jsonrpc': '2.0',
                'id': 2,
                'method': 'ledger_getSnapshotChainHeight',
                'params': 'null'
            }
            try:
                now = datetime.now()
                response = requests.post(url=url, json=body, headers=header)
            
                #print(response.status_code)
                if response.status_code == 200:
                    resp = response.json()
                    #print(resp)
                    respInfo = {
                        'node': node['name'],
                        'results': [
                            {
                                'datetime': now.strftime("%d/%m/%Y %H:%M:%S.%f")[:-3],
                                'status': True,
                                'result': resp
                            }
                        ]
                    }
                    lastData = getLastLocalData(localData, node['name'])
                    if lastData is not None:
                        respInfo['results'].append(lastData)

                    respData.append(respInfo)
                else:
                    print(node['name'] + ' not available (' + response.status_code + ')')
                    respInfo = {
                        'node': node['name'],
                        'results': [
                            {
                                'datetime': now.strftime("%d/%m/%Y %H:%M:%S.%f")[:-3],
                                'status': False,
                                'result': 'Code: ' + response.status_code
                            }
                        ]
                    }
                    respData.append(respInfo)
            except: # requests.exceptions.ConnectionError as e:
                respInfo = {
                        'node': node['name'],
                        'results': [
                            {
                                'datetime': now.strftime("%d/%m/%Y %H:%M:%S.%f")[:-3],
                                'status': False,
                                'result': 'Exception'
                            }
                        ]
                    }
                respData.append(respInfo)
                #pass
        writeJSON(fileName,respData)
        #print(respData)
        prepareMsg(respData)

requestNodeData()
