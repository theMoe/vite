# vite scripts

## Node Status [[VITE_nodeStatus.py](https://github.com/theMoe/vite/blob/main/002_NodeStatus/VITE_nodeStatus.py)]

### Requirements
* Python

### Install
Store the file anywhere you want to run it.

### Setup
**Variables**

Update the variable nodeDetails with the IP-addresses and the names of the node, which should be monitored. The name must not be exactly the name like the nodes name in the node_config.json. It's just for the message as information.
```python
nodeDetails = [
    {'name': '####', 'IP': '##.##.##.##'},
    {'name': '####', 'IP': '##.##.##.##'}
]
```

**Telegram**

Create telegram bot
1. Open Telegram
2. Open new conversation with @BotFather
3. Create new bot sending to @BotFather this text: /newbot
4. Answer to @BotFather with a name of your bot (e.g.: viteNews)
5. Answer to @BotFather with a username of your bot (e.g.: viteNews_bot)
6. Save the HTTP API that @BotFather has created.
7. Create a group on your Telegram and add your new bot to the group.
8. Add @my_id_bot to the same group.
9. Send /getgroupid to the group and save the Group ID.

Example URL request to test it:
```
https://api.telegram.org/bot[###YOUR BOT HTTP API saved from the step 6###])/sendMessage?chat_id=-[###YOUR GROUP ID saved from the step 9###]&text=Hello+world&user=User&password=Password&to=12345678
```
User, password and to are not needed.

Update variables in telgramMsg() function.
```python
def telegramMsg(msg):
    data = {
        'chat_id': '[###GROUP ID from step 9###]',
        'text': msg,
        'user': '[### optional, just use User###]',
        'password': '[### optional, just use Password###]',
        'to': '[### optional, just use 12345678###]'
    }
    url = 'https://api.telegram.org/bot[###BOT API from step 6###]/sendMessage'
    response = requests.post(url, data=data)
```

Messages will only be sent, if there is an issue. If there should be a message on every run, change the variable send to True or remove the if-condition at the end in the prepareMsg() function.
```python
def prepareMsg(data):
    msg = 'VITE-Nodes Update:'
    send = False
    ...
    if send == True:
        telegramMsg(msg)
```

### Run
**One time**
```
python3 VITE_nodeStatus.py
```
or
```
python VITE_nodeStatus.py
```
**On a regular basis e.g. cronjob [ubuntu]**

Create a cronjob by opening the crontab from the ubuntu command line
```
crontab -e
```
For every 15 minutes, just add the following example at the end of the cronjob file
```
0,15,30,45 * * * * python3 /home/[###ubuntu user###]/[###folders###]/VITE_nodeStatus.py
```
Hint: Esay way to create the right crontab time settings https://crontab.guru