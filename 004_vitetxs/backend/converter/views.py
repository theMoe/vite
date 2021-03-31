from datetime import date, datetime, timedelta, tzinfo
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from . import services
from .serializers import ConvertRequestSerializer, TransactionDownloadRequestSerializer, OrderDownloadRequestSerializer, DividendDownloadRequestSerializer, StakingDownloadRequestSerializer, MarketMakingDownloadRequestSerializer, TradingMiningDownloadRequestSerializer, InviteMiningDownloadRequestSerializer, AccountRequestSerializer
import pytz

class ViteConverter(APIView):  
    def post(self, request, format=None):
        print('post incoming')
        serializer = ConvertRequestSerializer(data=request.data)
        if serializer.is_valid():
            print('is valid')
            data = serializer.create(serializer.validated_data)
            try:
                print(data)
                response = services.loadDividends(data.vite_address)
                if response.status_code == 200:
                    resp = response.json()
                    if resp['data']['total'] == 0:
                        return Response('Keine Daten verfügbar, Vite Adresse falsch?', status=500)
                    else: 
                        return JsonResponse(resp, status=200)
                else:
                    return Response('Fehler!', status=response.status_code)
            except:
                return Response('Fehler in der loadDividends', status=500)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=500)

class ViteTransactionDownloader(APIView):
    def post(self, request, format=None):
        print('Transaction request incoming')
        print(request.data)
        serializer = TransactionDownloadRequestSerializer(data=request.data)
        if serializer.is_valid():
            #print(serializer.validated_data)
            data = serializer.create(serializer.validated_data)

            fromDate = None
            toDate = None
            if (data.toDate > datetime(1910,12,31,0,0,0,0, pytz.UTC) and data.fromDate > datetime(1910,12,31,0,0,0,0, pytz.UTC)):
                fromDate = int(datetime(data.fromDate.year, data.fromDate.month, data.fromDate.day, 0, 0, 0, 0, pytz.UTC).timestamp())
                toDate = int((datetime(data.toDate.year, data.toDate.month, data.toDate.day, 0, 0, 0, 0, pytz.UTC) + timedelta(days=1)).timestamp())

            try:
                #print(data)
                result = services.requestNodeData(data.viteAddress, data.transactionsPerRequest, data.pageMax, [fromDate, toDate], data.viteAddressSender)
                print(data.viteAddress)
                if 'file' in result:
                    response = HttpResponse(result['file'], content_type="text/csv")
                    # add a filename
                    response['Content-Disposition'] = "attachment; filename={0}.csv".format(data.viteAddress)
                    return response
                else:
                    if 'errorMsg' in result:
                        return Response({'msg': result['errorMsg']}, status=500)
                return Response({'msg': 'Error class: ViteDownloader'}, status=500)
            except:
                return Response({'msg': 'Error class: ViteDownloader'}, status=500)
        else:
            #print("notValid")
            #print(serializer.error_messages)
            errorMsg = {'Error': 'Something went wrong...'}
            for key, value in serializer.errors.items():
                if (key == 'viteAddress' and str(value).find('blank') > 0):
                    errorMsg = {key: 'VITE address is required.'}
            print(errorMsg)
            return Response(errorMsg, status=500)

class Markets(APIView):
    def post(self, request, format=None):
        print('Order request incoming')
        try:
            result = services.loadMarkets()
            if 'data' in result:
                return Response({'data': result['data']})
            else:
                if 'errorMsg' in result:
                    return Response({'msg': result['errorMsg']}, status=500)
            return Response({'msg': 'Error class: Markets'}, status=500)
        except:
                return Response({'msg': 'Error class: Markets'}, status=500)

class ViteOrdersDownloader(APIView):
    def post(self, request, format=None):
        print('Order request incoming')
        #print(request.data)
        serializer = OrderDownloadRequestSerializer(data=request.data)
        if serializer.is_valid():
            #print(serializer.validated_data)
            data = serializer.create(serializer.validated_data)
            fromDate = None
            toDate = None
            if (data.toDate > datetime(1910,12,31,0,0,0,0, pytz.UTC) and data.fromDate > datetime(1910,12,31,0,0,0,0, pytz.UTC)):
                fromDate = int(datetime(data.fromDate.year, data.fromDate.month, data.fromDate.day, 0, 0, 0, 0, pytz.UTC).timestamp())
                toDate = int((datetime(data.toDate.year, data.toDate.month, data.toDate.day, 0, 0, 0, 0, pytz.UTC) + timedelta(days=1)).timestamp())

            try:
                #print(data)
                result = services.loadOrders(data.viteAddress, data.limit, [fromDate, toDate], data.sellBuy, data.symbol, data.quoteToken, data.tradeToken, data.orderStatus)

                if 'file' in result:
                    response = HttpResponse(result['file'], content_type="text/csv")
                    # add a filename
                    response['Content-Disposition'] = "attachment; filename=orders_{0}.csv".format(data.viteAddress)
                    return response
                else:
                    if 'errorMsg' in result:
                        return Response({'msg': result['errorMsg']}, status=500)
                return Response({'msg': 'Error class: ViteOrdersDownloader'}, status=500)
            except:
                return Response({'msg': 'Error class: ViteOrdersDownloader'}, status=500)
        else:
            print("notValid")
            return Response(serializer.errors, status=500)

class ViteDividendsDownloader(APIView):
    def post(self, request, format=None):
        print('Order request incoming')
        #print(request.data)
        serializer = DividendDownloadRequestSerializer(data=request.data)
        if serializer.is_valid():
            #print(serializer.validated_data)
            data = serializer.create(serializer.validated_data)

            try:
                #print(data)
                result = services.loadDividends(data.viteAddress)

                if 'file' in result:
                    response = HttpResponse(result['file'], content_type="text/csv")
                    # add a filename
                    response['Content-Disposition'] = "attachment; filename=dividends_{0}.csv".format(data.viteAddress)
                    return response
                else:
                    if 'errorMsg' in result:
                        return Response({'msg': result['errorMsg']}, status=500)
                return Response({'msg': 'Error class: ViteDividendsDownloader'}, status=500)
            except:
                return Response({'msg': 'Error class: ViteDividendsDownloader'}, status=500)
        else:
            errorMsg = {'Error': 'Something went wrong...'}
            for key, value in serializer.errors.items():
                if (key == 'viteAddress' and str(value).find('blank') > 0):
                    errorMsg = {key: 'VITE address is required.'}
            print(errorMsg)
            return Response(errorMsg, status=500)

class ViteStakingsDownloader(APIView):
    def post(self, request, format=None):
        print('Order request incoming')
        #print(request.data)
        serializer = StakingDownloadRequestSerializer(data=request.data)
        if serializer.is_valid():
            #print(serializer.validated_data)
            data = serializer.create(serializer.validated_data)

            try:
                #print(data)
                result = services.loadStakingData(data.viteAddress)

                if 'file' in result:
                    response = HttpResponse(result['file'], content_type="text/csv")
                    # add a filename
                    response['Content-Disposition'] = "attachment; filename=stakings_{0}.csv".format(data.viteAddress)
                    return response
                else:
                    if 'errorMsg' in result:
                        return Response({'msg': result['errorMsg']}, status=500)
                return Response({'msg': 'Error class: ViteStakingsDownloader'}, status=500)
            except:
                return Response({'msg': 'Error class: ViteStakingsDownloader'}, status=500)
        else:
            errorMsg = {'Error': 'Something went wrong...'}
            for key, value in serializer.errors.items():
                if (key == 'viteAddress' and str(value).find('blank') > 0):
                    errorMsg = {key: 'VITE address is required.'}
            print(errorMsg)
            return Response(errorMsg, status=500)

class ViteMarketMakingDownloader(APIView):
    def post(self, request, format=None):
        print('Order request incoming')
        #print(request.data)
        serializer = MarketMakingDownloadRequestSerializer(data=request.data)
        if serializer.is_valid():
            #print(serializer.validated_data)
            data = serializer.create(serializer.validated_data)

            try:
                #print(data)
                result = services.loadMarketMakingData(data.viteAddress)

                if 'file' in result:
                    response = HttpResponse(result['file'], content_type="text/csv")
                    # add a filename
                    response['Content-Disposition'] = "attachment; filename=marketMaking_{0}.csv".format(data.viteAddress)
                    return response
                else:
                    if 'errorMsg' in result:
                        return Response({'msg': result['errorMsg']}, status=500)
                return Response({'msg': 'Error class: ViteMarketMakingDownloader'}, status=500)
            except:
                return Response({'msg': 'Error class: ViteMarketMakingDownloader'}, status=500)
        else:
            errorMsg = {'Error': 'Something went wrong...'}
            for key, value in serializer.errors.items():
                if (key == 'viteAddress' and str(value).find('blank') > 0):
                    errorMsg = {key: 'VITE address is required.'}
            print(errorMsg)
            return Response(errorMsg, status=500)

class ViteTradingMiningDownloader(APIView):
    def post(self, request, format=None):
        print('Order request incoming')
        #print(request.data)
        serializer = TradingMiningDownloadRequestSerializer(data=request.data)
        if serializer.is_valid():
            #print(serializer.validated_data)
            data = serializer.create(serializer.validated_data)

            try:
                #print(data)
                result = services.loadTradingMiningData(data.viteAddress)

                if 'file' in result:
                    response = HttpResponse(result['file'], content_type="text/csv")
                    # add a filename
                    response['Content-Disposition'] = "attachment; filename=tradingMining_{0}.csv".format(data.viteAddress)
                    return response
                else:
                    if 'errorMsg' in result:
                        return Response({'msg': result['errorMsg']}, status=500)
                return Response({'msg': 'Error class: ViteTradingMiningDownloader'}, status=500)
            except:
                return Response({'msg': 'Error class: ViteTradingMiningDownloader'}, status=500)
        else:
            errorMsg = {'Error': 'Something went wrong...'}
            for key, value in serializer.errors.items():
                if (key == 'viteAddress' and str(value).find('blank') > 0):
                    errorMsg = {key: 'VITE address is required.'}
            print(errorMsg)
            return Response(errorMsg, status=500)

class ViteInviteMiningDownloader(APIView):
    def post(self, request, format=None):
        print('Order request incoming')
        #print(request.data)
        serializer = InviteMiningDownloadRequestSerializer(data=request.data)
        if serializer.is_valid():
            #print(serializer.validated_data)
            data = serializer.create(serializer.validated_data)

            try:
                #print(data)
                result = services.loadInviteMiningData(data.viteAddress)

                if 'file' in result:
                    response = HttpResponse(result['file'], content_type="text/csv")
                    # add a filename
                    response['Content-Disposition'] = "attachment; filename=inviteMining_{0}.csv".format(data.viteAddress)
                    return response
                else:
                    if 'errorMsg' in result:
                        return Response({'msg': result['errorMsg']}, status=500)
                return Response({'msg': 'Error class: ViteInviteMiningDownloader'}, status=500)
            except:
                return Response({'msg': 'Error class: ViteInviteMiningDownloader'}, status=500)
        else:
            errorMsg = {'Error': 'Something went wrong...'}
            for key, value in serializer.errors.items():
                if (key == 'viteAddress' and str(value).find('blank') > 0):
                    errorMsg = {key: 'VITE address is required.'}
            print(errorMsg)
            return Response(errorMsg, status=500)

class ViteAccount(APIView):  
    def post(self, request, format=None):
        print('post incoming')
        serializer = AccountRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.create(serializer.validated_data)
            try:
                print(data)
                resp = services.getAccountInfo(data.viteAddress)
                
                return JsonResponse(resp, status=200)
            except:
                return Response('Error in class ViteAccount', status=500)
        else:
            return Response(serializer.errors, status=500) 

class ViteSBP(APIView):  
    def post(self, request, format=None):
        print('post incoming')
        try:
            resp = services.getSBP()
            
            return JsonResponse(resp, status=200)
        except:
            return Response('Error in class ViteAccount', status=500)
 
        
    