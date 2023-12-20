# Weather Forecast API
Get accurate weather forecasts for any location with our Weather Forecast API. Retrieve current conditions, hourly and daily forecasts, and historical weather data for any location in the world.

## Sample API Request

```python
import requests

headers = {
    'Authorization': 'Api-Key YOUR_API_KEY'
}

params = {
    'lat': '32.0411366',
    'lon': '76.710075'
}

response = requests.get('https://api.tinyapi.co/v1/weather/today/?lat=33.44&lon=-94.04', headers=headers, params=params)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")
```

## Sample API Response

```json
{
    "location": {
        "name": "New York",
        "region": "New York",
        "country": "United States",
        "latitude": 40.71,
        "longitude": -74.01
    },
    "current": {
        "temperature": 23,
        "feelsLike": 22,
        "humidity": 65,
        "windSpeed": 10,
        "windDirection": "W",
        "visibility": 16,
        "pressure": 1015,
        "uvIndex": 3,
        "description": "Partly cloudy"
    },
    "forecast": [
        {
            "date": "2023-04-19",
            "minTemperature": 19,
            "maxTemperature": 27,
            "precipitationProbability": 10,
            "weatherDescription": "Partly cloudy"
        },
        {
            "date": "2023-04-20",
            "minTemperature": 20,
            "maxTemperature": 26,
            "precipitationProbability": 5,
            "weatherDescription": "Sunny"
        }
    ]
}
```

Use the Weather Forecast API to get accurate weather forecasts, current conditions, and weather alerts for any location worldwide. It's perfect for travel planning, outdoor activities, and event management.

## Integration

_Easily integrate Tiny API into your projects_

Integrating Tiny API into your projects is a straightforward process. Follow these simple steps, and you'll have the power of Tiny API at your fingertips.

### Step 1: Sign Up and Get Your API Key

To get started with Tiny API, you'll first need to sign up for an account on our website. Once you've signed up, you'll receive an API key, which you'll need to include in your API requests for authentication.

### Step 2: Choose Your API

Next, you'll need to choose the API you want to integrate into your project. Explore our extensive catalog of APIs, and find the one that best suits your needs. Make sure to familiarize yourself with the API documentation, which includes important information on the available endpoints, request parameters, and response formats.

### Step 3: Make API Requests

With your API key and chosen API in hand, you're now ready to start making API requests. You can use any programming language or tool that supports HTTP requests to make calls to the Tiny API endpoints. Remember to include your API key in the request headers for authentication.

