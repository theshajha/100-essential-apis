import datetime

import requests
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework.response import Response
from sentry_sdk import capture_exception

from rest_framework.views import APIView
from .throttles import CustomScopedRateThrottle

from rest_framework.permissions import BasePermission


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        # Implement custom permission logic
        return True


class BaseWeatherAPIView(APIView):
    throttle_classes = [CustomScopedRateThrottle]
    permission_classes = [CustomPermission]

    def get_weather_data(self, lat, lon, endpoint):
        # Use your own weather API endpoint here.
        if endpoint == 'today':
            exclude = 'minutely,hourly,alerts'
        elif endpoint == 'verbose':
            exclude = 'alerts'
        elif endpoint == 'week':
            exclude = 'minutely,hourly,current,alerts'
        elif endpoint == 'hourly':
            exclude = 'minutely,current,daily,alerts'
        else:
            exclude = 'minutely'
        try:
            url = (f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={exclude}"
                   f"&appid={settings.OPEN_WEATHER_API_KEY}")
            response = requests.get(url)
            data = response.json()
            transformed_data = self.transform_data(data, lat, lon)
            return transformed_data
        except Exception as e:
            capture_exception(e)
            return {"error": "Something went wrong while fetching weather data. Error - " + str(e)}

    def transform_data(self, data, lat, lon):
        # Transformation function to convert OpenWeather data into desired format
        transformed_data = {
            "location": {
                "name": "Unknown",
                "region": data['timezone'],
                "country": "Unknown",
                "latitude": lat,
                "longitude": lon,
            },
            "current": {
                "temperature": {
                    "celsius": data['current']['temp'] - 273.15,
                    "fahrenheit": (data['current']['temp'] - 273.15) * 9 / 5 + 32
                },
                "feelsLike": {
                    "celsius": data['current']['feels_like'] - 273.15,
                    "fahrenheit": (data['current']['feels_like'] - 273.15) * 9 / 5 + 32
                },
                "humidity": data['current']['humidity'],
                "windSpeed": data['current']['wind_speed'],
                "windDirection": "N/A",
                "visibility": data['current'].get('visibility', 'N/A'),
                "pressure": data['current']['pressure'],
                "uvIndex": data['current']['uvi'],
                "description": data['daily'][0]['summary']
            },
            "forecast": [
                {
                    "date": datetime.datetime.fromtimestamp(forecast['dt']).strftime('%d-%m-%Y'),
                    "minTemperature": {
                        "celsius": forecast['temp']['min'] - 273.15,
                        "fahrenheit": (forecast['temp']['min'] - 273.15) * 9 / 5 + 32
                    },
                    "maxTemperature": {
                        "celsius": forecast['temp']['max'] - 273.15,
                        "fahrenheit": (forecast['temp']['max'] - 273.15) * 9 / 5 + 32
                    },
                    "precipitationProbability": forecast.get('pop', 'N/A'),
                    "weatherDescription": forecast['weather'][0]['description']
                } for forecast in data['daily']
            ]
        }
        return transformed_data


class TodayWeatherAPIView(BaseWeatherAPIView):
    @method_decorator(cache_page(60 * 60 * 1))  # Cache this view for 1 hours
    @method_decorator(vary_on_headers('lat', 'lon'))  # Vary on latitude and longitude headers
    def get(self, request, *args, **kwargs):
        lat = request.GET.get('lat', None)
        lon = request.GET.get('lon', None)
        if not lat or not lon:
            return Response({"error": "Latitude and Longitude are required parameters"}, status=400)
        data = self.get_weather_data(lat, lon, 'today')
        return Response(data)


class VerboseWeatherAPIView(BaseWeatherAPIView):
    @method_decorator(cache_page(60 * 60 * 1))  # Cache this view for 1 hours
    @method_decorator(vary_on_headers('lat', 'lon'))  # Vary on latitude and longitude headers
    def get(self, request, *args, **kwargs):
        lat = request.GET.get('lat', None)
        lon = request.GET.get('lon', None)
        if not lat or not lon:
            return Response({"error": "Latitude and Longitude are required parameters"}, status=400)
        data = self.get_weather_data(lat, lon, 'verbose')
        return Response(data)


class WeekWeatherAPIView(BaseWeatherAPIView):
    @method_decorator(cache_page(60 * 60 * 1))  # Cache this view for 1 hours
    @method_decorator(vary_on_headers('lat', 'lon'))  # Vary on latitude and longitude headers
    def get(self, request, *args, **kwargs):
        lat = request.GET.get('lat', None)
        lon = request.GET.get('lon', None)
        if not lat or not lon:
            return Response({"error": "Latitude and Longitude are required parameters"}, status=400)
        data = self.get_weather_data(lat, lon, 'week')
        return Response(data)


class HourlyWeatherAPIView(BaseWeatherAPIView):
    @method_decorator(cache_page(60 * 60 * 1))  # Cache this view for 1 hours
    @method_decorator(vary_on_headers('lat', 'lon'))  # Vary on latitude and longitude headers
    def get(self, request, *args, **kwargs):
        lat = request.GET.get('lat', None)
        lon = request.GET.get('lon', None)
        if not lat or not lon:
            return Response({"error": "Latitude and Longitude are required parameters"}, status=400)
        data = self.get_weather_data(lat, lon, 'hourly')
        return Response(data)
