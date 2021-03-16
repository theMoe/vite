from django.urls import include, path
from . import views

urlpatterns = [
    path('convert/', views.ViteConverter.as_view()),
    path('transactions/', views.ViteTransactionDownloader.as_view()),
    path('account/', views.ViteAccount.as_view()),
    path('sbp/', views.ViteSBP.as_view()),
    path('orders/', views.ViteOrdersDownloader.as_view()),
    path('dividends/', views.ViteDividendsDownloader.as_view()),
    path('mining/staking/', views.ViteStakingsDownloader.as_view()),
    path('mining/marketmaking/', views.ViteMarketMakingDownloader.as_view()),
    path('mining/trading/', views.ViteTradingMiningDownloader.as_view()),
    path('mining/invite/', views.ViteInviteMiningDownloader.as_view()),
]