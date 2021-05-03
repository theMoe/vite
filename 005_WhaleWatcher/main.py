import websocket
import asyncio
import requests
import json
import math
import tweepy
import logging
import threading
from datetime import date, datetime
from discord_webhook import DiscordWebhook

try:
    import thread
except ImportError:
    import _thread as thread
import time

# Twitter
consumer_key = ''
consumer_secret = ''
bearer_token = ''
access_token = ''
access_token_secret = ''

knownAccounts = {
    'vite_0ab5b9c50b27647538cbb7918980c1dd4c281b1a53b2a7c4a1': 'Binance',
    'vite_8588d741af13504d79154312f9f4838789aa06d3d0e1b4bea1': 'Team Lock',
    'vite_a4ddd2bb327eb9b5a96ecef75489247f1f59610c22af477088': 'Ecosystem Fund',
    'vite_0000000000000000000000000000000000000003f6af7459b9': 'Quota & Mining',
    'vite_0000000000000000000000000000000000000006e82b8ba657': 'ViteX',
    'vite_e578c937ad5bb207503e4cc441cd605f3aecf3227f955a1ea7': 'Marketing',
    'vite_f47b4cf5dcf160341aa7bcad1a286a8ebce14f75c47ea026b0': 'Upbit',
    'vite_0000000000000000000000000000000000000004d28108e76b': 'SBP',
    'vite_f932c4a43a207cf0c49da5fe2dd0e95204d58029ef62d76265': 'okexpool',
    'vite_3e315d18f6453b08ce0f2785673342a7a7d72aaabace0d5452': 'Airdrop',
    'vite_3de962da3a284eade8ddc8d5fef37f67996f2c330342f8da06': 'ERC20 Swap',
    'vite_cc73798810381bee8e5aeb7a5f7a772b02a9048a355d6b1f92': 'Okex',
    'vite_591e456aa84fccd65e4c916c258ef3b80fadd94eab6f37518c': 'Binance',
    'vite_1737bb7abc4883cc2f415a804f80274d3a725a68a5bee5bad3': 'Full Node Rewards',  # new
    'vite_86f729c9b7dda636e46b7ae738785be87f71390f532828ace9': 'Full Node Rewards',
}

fullNodeRewardAddress = ['vite_86f729c9b7dda636e46b7ae738785be87f71390f532828ace9',
                         'vite_1737bb7abc4883cc2f415a804f80274d3a725a68a5bee5bad3']

tokenIDs = {
    'tti_5649544520544f4b454e6e40': 'VITE'
}


server = '0.0.0.0'
websocket_url = f'ws://{server}:41420/'
rest_url = f'http://{server}:48132'

last_fullnode_reward_date = None
last_fullnode_reward_amount = 0

class NoNeededValueProvided(Exception):
     pass

class WebSocketClient():
    def tweet(self, message):
        auth=tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api=tweepy.API(auth)
        #
        # Die nachfolgende Zeile tweeted auf meinen privaten Account, bitte vorsichtig sein!
        #
        api.update_status(status=message)
        #
        print('message sent')
    
    
    def __init__(self, ):
        # websocket.enableTrace(True)
        ws = websocket.WebSocketApp(websocket_url,
                                    on_message=self.on_message)
        self.ws = ws
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    def get_header(self):
        header = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json'
        }
        return header

    def get_chunk_response(self, param):
        response = requests.post(rest_url, headers=self.get_header(), data=json.dumps({"jsonrpc": "2.0", "id": 0, "method":"ledger_getChunks", "params": [param, param]})).json()
        
        if ('result' not in response or len(response['result']) == 0 or 'AccountBlocks' not in response['result'][0] or response['result'][0]['AccountBlocks'] is None):
            raise NoNeededValueProvided
        else:
            return response['result'][0]['AccountBlocks']

    def get_account_block_response(self, data):
        response = requests.post(rest_url, headers=self.get_header(), data=json.dumps({"jsonrpc": "2.0", "id": 2, "method":"ledger_getAccountBlockByHash", "params": [data]}))
        return response.json()['result']

    def on_message(self, ws, message):
        global last_fullnode_reward_date
        global last_fullnode_reward_amount
        
        result = int(json.loads(message)['result'])
        
        try:
            chunk_response = self.get_chunk_response(result)

            for accountBlock in chunk_response: 

                if (accountBlock['blockType'] == 2):
                    if accountBlock['accountAddress'] in fullNodeRewardAddress and accountBlock['tokenId'] == 'tti_5649544520544f4b454e6e40' and float(accountBlock['amount']) < 30000000000000000000:
                        if accountBlock['amount'] != last_fullnode_reward_amount and last_fullnode_reward_date is not date.today().strftime("%d/%m/%Y"):
                            last_fullnode_reward_date = date.today().strftime("%d/%m/%Y")
                            last_fullnode_reward_amount = accountBlock['amount']
                            amount_decimal = float(last_fullnode_reward_amount) / math.pow(10, 18)
                            
                            amount_string = f"{amount_decimal:,.4f}"
                            print('Daily Reward', amount_string)

                            msg = f'\U0001F4E3\U0001F4E3\U0001F4E3\n\nDaily Full Node Rewards Distributed \U00002705\n\n{amount_string} $VITE per Full Node \U0001F3C3'

                            webhook = DiscordWebhook(
                                url='https://discord.com/api/webhooks/[API KEY]', content=msg)
                            webhook.execute()
                            self.tweet(msg)
                        else:
                            print('Daily Reward already sent')
                        
                        continue

                    data_hash = accountBlock['hash']
                    account_block_response = self.get_account_block_response(data_hash)
                    amount = account_block_response['amount']

                    if (amount != '0'):
                            
                        toAddress = account_block_response['toAddress']
                        fromAddress = account_block_response['fromAddress']
                        symbol = account_block_response['tokenInfo']['tokenSymbol']
                        tokenIndex = account_block_response['tokenInfo']['index']
                        tokenSymbol = symbol

                        if (symbol not in ['VITE', 'VX', 'VCP']):
                            tokenSymbol = symbol + '-' + '{:03}'.format(tokenIndex)

                        decimals = int(account_block_response['tokenInfo']['decimals'])
                        decimal_amount = float(amount) / math.pow(10, decimals)

                        if (symbol in ['VITE', 'VX'] and decimal_amount < 10000):
                            continue    

                        print('-------------------')
                        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                        print(tokenSymbol, decimal_amount, data_hash)

                        value_request_json = requests.get(f'https://api.vitex.net/api/v2/exchange-rate?tokenSymbols={tokenSymbol}').json()['data'][0]

                        usdRate = value_request_json['usdRate']
                        usdValue = float(decimal_amount) * float(usdRate)

                        usdStr = '' if symbol == 'USDT' else '(' + f"{usdValue:,.2f}" + ' USDT) '

                        if (decimal_amount % 1 == 0):
                            decimal_amount = f"{decimal_amount:,.0f}"
                        else:
                            decimal_amount = f"{decimal_amount:,.4f}"

                        fromWalletStr = knownAccounts[fromAddress] if account_block_response[
                            'fromAddress'] in knownAccounts else 'unknown address'
                        toWalletStr = knownAccounts[toAddress] if account_block_response[
                            'toAddress'] in knownAccounts else 'unknown address'

                        fromToStr = f"from {fromWalletStr} to {toWalletStr}"

                        print(fromToStr, usdStr)

                        msg_base = f'transaction {fromToStr} at block height {result:,} on $VITE chain\n\n{decimal_amount} {symbol} {usdStr}'
                        msg_hash = f'Details at https://explorer.vite.net/transaction/{data_hash}'

                        if (usdValue >= 500000):
                            msg = f'\U0001F6A8\U0001F514\U0001F6A8\U0001F514\U0001F6A8\n\nvitetxs.de noticed a big \U0001F433 {msg_base}\n\U0001F3C3\U0001F3C3\U0001F3C3\n{msg_hash}'

                            webhook = DiscordWebhook(
                                url='https://discord.com/api/webhooks/[API KEY]', content=msg)
                            webhook.execute()
                            self.tweet(msg)
                        elif (usdValue >= 100000):
                            msg = f'\U0001F6A8\U0001F514\U0001F6A8\n\nvitetxs.de noticed a medium \U0001F42C {msg_base}\n\U0001F3C3\U0001F3C3\n{msg_hash}'

                            webhook = DiscordWebhook(
                                url='https://discord.com/api/webhooks/[API KEY]', content=msg)
                            webhook.execute()
                            self.tweet(msg)
                        elif (usdValue >= 50000):
                            print('Very small')
                            msg = f'\U0001F514\U0001F514\n\nvitetxs.de noticed a small \U0001F420 {msg_base}\n\U0001F3C3\n{msg_hash}'

                            webhook = DiscordWebhook(
                                url='https://discord.com/api/webhooks/[API KEY]', content=msg)
                            webhook.execute()
                            self.tweet(msg)
                        else:
                            print('Too small')

            return

        except ValueError:
            print('Something is wrong with received data')
            return
        except NoNeededValueProvided:
            print('API returned an chunk response without needed account blocks')
            return
        except:
            print('Something went wrong')
            return

    def run(self, *args):
        global driver
        driver = True
        while driver:
            try:
                time.sleep(1)
                self.ws.send('{"jsonrpc":"2.0","id":17,"method":"ledger_getSnapshotChainHeight","params":null}')
            except KeyboardInterrupt:
                driver = False
        time.sleep(1)
        self.ws.close()
        print('thread terminating...')

    def on_open(self, foo):
        thread.start_new_thread(self.run, ())


websocket_client = WebSocketClient()
