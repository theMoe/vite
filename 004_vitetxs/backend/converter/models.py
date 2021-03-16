from django.db import models

class AccountRequest:
    def __init__(self, viteAddress):
        self.viteAddress = viteAddress

    def __str__(self):
        return self.viteAddress

class ConvertRequest:
    def __init__(self, from_date, to_date, vite_address):
        self.from_date = from_date
        self.to_date = to_date
        self.vite_address = vite_address

    def __str__(self):
        return self.vite_address

class TransactionDownloadRequest:
    def __init__(self, fromDate, toDate, viteAddress, pageMax, transactionsPerRequest):
        self.fromDate = fromDate
        self.toDate = toDate
        self.viteAddress = viteAddress
        self.pageMax = pageMax
        self.transactionsPerRequest = transactionsPerRequest

    def __str__(self):
        return self.viteAddress

class OrderDownloadRequest:
    def __init__(self, fromDate, toDate, viteAddress, limit, sellBuy):
        self.fromDate = fromDate
        self.toDate = toDate
        self.viteAddress = viteAddress
        self.limit = limit
        self.sellBuy = sellBuy
        #self.orderStatus = orderStatus

    def __str__(self):
        return self.viteAddress

class DividendDownloadRequest:
    def __init__(self, viteAddress):
        self.viteAddress = viteAddress

    def __str__(self):
        return self.viteAddress

class StakingDownloadRequest:
    def __init__(self, viteAddress):
        self.viteAddress = viteAddress

    def __str__(self):
        return self.viteAddress

class MarketMakingDownloadRequest:
    def __init__(self, viteAddress):
        self.viteAddress = viteAddress

    def __str__(self):
        return self.viteAddress

class TradingMiningDownloadRequest:
    def __init__(self, viteAddress):
        self.viteAddress = viteAddress

    def __str__(self):
        return self.viteAddress

class InviteMiningDownloadRequest:
    def __init__(self, viteAddress):
        self.viteAddress = viteAddress

    def __str__(self):
        return self.viteAddress