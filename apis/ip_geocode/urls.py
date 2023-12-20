from django.urls import path
from .temp import *

app_name = 'ip_geocode'

urlpatterns = [
    path('', IPGeocodeView.as_view(), name='ip_geocode_automatic'),
    path('<str:ip_address>/', IPGeocodeView.as_view(), name='ip_geocode_manual'),
]