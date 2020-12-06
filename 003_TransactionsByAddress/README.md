## Transactions by Address [[VITE_transactionsByAddress.py](https://github.com/theMoe/vite/blob/main/003_TransactionsByAddress/VITE_transactionsByAddress.py)]

The script creates a JSON- and a CSV-file with all transactions for a specific VITE_ADDRESS.

### Requirements
* Python package pandas
```
pip install pandas
```

### Install
Store the file anywhere you want to run it.

### Run
Just run
```
python3 VITE_transactionsByAddress.py --vaddr VITE_ADDRESS --nodeIP VITE_NODE_IP
```

Help
```
python3 VITE_transactionsByAddress.py --help
```

Additional options (Only, if both dates are given, they will be used):
--fromDate 2020-12-01
--toDate 2020-12-04