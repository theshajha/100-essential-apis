from django.urls import path
from .views import TodayWeatherAPIView, VerboseWeatherAPIView, WeekWeatherAPIView, HourlyWeatherAPIView

urlpatterns = [
    path('today/', TodayWeatherAPIView.as_view(), name='weather-today'),
    path('verbose/', VerboseWeatherAPIView.as_view(), name='weather-verbose'),
    path('week/', WeekWeatherAPIView.as_view(), name='weather-week'),
    path('hourly/', HourlyWeatherAPIView.as_view(), name='weather-hourly'),
    # ... other paths ...
]
