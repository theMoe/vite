"""vitemoe URL Configuration
"""
from django.urls import include, path

urlpatterns = [
    path('api/', include('converter.urls')),
]
