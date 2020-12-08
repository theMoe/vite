## Node Status Scriptable [[VITE_nodeStatus.scriptable](https://github.com/theMoe/vite/blob/main/001_NodeStatusScriptable/VITE_nodeStatus.scriptable), [VITE_nodeStatus_scriptable.txt](https://github.com/theMoe/vite/blob/main/001_NodeStatusScriptable/VITE_nodeStatus_scriptable.txt)]

### Requirements
Download Scriptable from the App Store
https://scriptable.app/

### Install
Import .scriptable or copy code from .txt

### Setup
**Variable**

Update the variable nodeDetail with the IP-adresses and name of the node. The node name HAVE TO be the same like in node_config.json.
```
const nodeDetail = [['x.x.x.ip1', 'nodeName1'],['...', '....']]
```

If the font size is too small, just change:
```
const fontSize = 7
```

If you want to get information about the online ratio of the nodes from the last complete cycle, just set loadCycleOnlineRatio to true. A JSON-file cycleData.json will be stored on your phone. As the request usualy takes a little bit longer, the cycle information will only be requested once a day.
```
const loadCycleOnlineRatio = true
```

### Run
To run the code, just click it in Scriptable. You can also add it to your home screen.