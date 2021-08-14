import requests
import random
import datetime

def get_url(ip):
    return 'http://' + ip + ':48132'

def get_header():
    header = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json'
    }
    return header

def try_ip(ip):
    url = get_url(ip)
    header = get_header()
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

def get_node_ip():
    backupIP = ['170.106.33.134', '150.109.116.1', '150.109.51.8']
    random.shuffle(backupIP)
    for ip in backupIP:
        if try_ip(ip) == True:
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
                    if try_ip(result['ip']) == True:
                        print('good ip ' + result['ip'])
                        return result['ip']
                    else:
                        print('bad ip ' + result['ip'])

    return False
