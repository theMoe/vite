from rest_framework import serializers

from .models import ConvertRequest, TransactionDownloadRequest, OrderDownloadRequest, DividendDownloadRequest, StakingDownloadRequest, MarketMakingDownloadRequest, TradingMiningDownloadRequest, InviteMiningDownloadRequest, AccountRequest

class AccountRequestSerializer(serializers.Serializer):
    viteAddress = serializers.CharField(max_length=128)

    def create(self, validated_data):
        return AccountRequest(**validated_data)

    def __str__(self):
        return self.viteAddress

class ConvertRequestSerializer(serializers.Serializer):
    from_date = serializers.DateField()
    to_date = serializers.DateField()
    vite_address = serializers.CharField(max_length=128)

    def create(self, validated_data):
        return ConvertRequest(**validated_data)

    def __str__(self):
        return self.vite_address

class TransactionDownloadRequestSerializer(serializers.Serializer):
    viteAddress = serializers.CharField(max_length=128)
    viteAddressSender = serializers.ListField(
        child = serializers.CharField(max_length=128)
    )
    fromDate = serializers.DateTimeField()
    toDate = serializers.DateTimeField()
    transactionsPerRequest = serializers.IntegerField()
    pageMax = serializers.IntegerField()

    def create(self, validated_data):
        return TransactionDownloadRequest(**validated_data)

    def __str__(self):
        return self.viteAddress

class OrderDownloadRequestSerializer(serializers.Serializer):
    viteAddress = serializers.CharField(max_length=128)
    fromDate = serializers.DateTimeField()
    toDate = serializers.DateTimeField()
    limit = serializers.IntegerField()
    sellBuy = serializers.IntegerField(allow_null=True)
    symbol = serializers.CharField(allow_null=True, max_length=128)
    quoteToken = serializers.CharField(allow_null=True, max_length=128)
    tradeToken = serializers.CharField(allow_null=True, max_length=128)
    orderStatus = serializers.IntegerField(allow_null=True)

    def create(self, validated_data):
        return OrderDownloadRequest(**validated_data)

    def __str__(self):
        return self.viteAddress

class DividendDownloadRequestSerializer(serializers.Serializer):
    viteAddress = serializers.CharField(max_length=128)

    def create(self, validated_data):
        return DividendDownloadRequest(**validated_data)

    def __str__(self):
        return self.viteAddress

class StakingDownloadRequestSerializer(serializers.Serializer):
    viteAddress = serializers.CharField(max_length=128)

    def create(self, validated_data):
        return StakingDownloadRequest(**validated_data)

    def __str__(self):
        return self.viteAddress

class MarketMakingDownloadRequestSerializer(serializers.Serializer):
    viteAddress = serializers.CharField(max_length=128)

    def create(self, validated_data):
        return MarketMakingDownloadRequest(**validated_data)

    def __str__(self):
        return self.viteAddress

class TradingMiningDownloadRequestSerializer(serializers.Serializer):
    viteAddress = serializers.CharField(max_length=128)

    def create(self, validated_data):
        return TradingMiningDownloadRequest(**validated_data)

    def __str__(self):
        return self.viteAddress

class InviteMiningDownloadRequestSerializer(serializers.Serializer):
    viteAddress = serializers.CharField(max_length=128)

    def create(self, validated_data):
        return InviteMiningDownloadRequest(**validated_data)

    def __str__(self):
        return self.viteAddress