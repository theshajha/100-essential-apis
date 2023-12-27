from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import *

app_name = 'apis'

router = DefaultRouter()
# router.register('apis', ApiListViewSet, basename='apis_list')

# urlpatterns now includes the router.urls and the 'ip-geocode' path
urlpatterns = [
                  path('ip-geocode/', include('apis.ip_geocode.urls')),
                  path('weather/', include('apis.weather_forecast.urls')),
                  path('domain-tracker/', include('apis.domain_tracker.urls')),
              ] + router.urls
