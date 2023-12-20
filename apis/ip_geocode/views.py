import json
from django.http import HttpRequest

from rest_framework.response import Response
from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, throttle_classes
from rest_framework import permissions
from rest_framework import serializers
import pycountry
import phonenumbers
from rest_framework.throttling import AnonRateThrottle
from sentry_sdk import capture_exception, capture_message
from django.conf import settings
from django.core.cache import cache


# from ipware import get_client_ip

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip, True


@throttle_classes([AnonRateThrottle])
@permission_classes((permissions.AllowAny,))
class IPGeocodeView(APIView):

    def get(self, request, ip_address=None, format=None):
        # Use a settings variable for the path to the GeoLite2-City database
        geo_db_path = getattr(settings, 'GEOLITE2_CITY_DB_PATH', 'apis/ip_geocode/GeoLite2-City.mmdb')
        reader = Reader(geo_db_path)

        # If no IP address is provided, use the utility function to get the client's IP
        if not ip_address:
            ip_address, is_routable = get_client_ip(request)
            if not ip_address or not is_routable:
                return Response({'error': 'Unable to determine or use the provided IP address.'}, status=400)

        # Check if we have the data in cache first
        cache_key = f"geoip_data_{ip_address}"
        data = cache.get(cache_key)
        if data:
            reader.close()
            return Response(data)

        # If not in cache, process the request
        try:
            response = reader.city(ip_address)
        except AddressNotFoundError:
            return Response({"error": "IP address not found", 'ip_address': str(ip_address)}, status=404)
        except Exception as e:
            return Response(
                {"error": "An error occurred while processing the IP address.", 'ip_address': str(ip_address)},
                status=500)

        data = build_geoip_data(response, ip_address)

        # Save the data in cache for future requests
        timeout = getattr(settings, 'GEOIP_CACHE_TIMEOUT', 86400)  # Default to 24 hours
        cache.set(cache_key, data, timeout=timeout)

        reader.close()

        return Response(data)


def build_geoip_data(geoip_response, ip_address):
    data = {
        "ip": str(ip_address),
        "country_code": geoip_response.country.iso_code if geoip_response.country else None,
        "country_name": geoip_response.country.name if geoip_response.country else "Unknown",
        "region_code": geoip_response.subdivisions.most_specific.iso_code if geoip_response.subdivisions.most_specific else None,
        "region_name": geoip_response.subdivisions.most_specific.name if geoip_response.subdivisions.most_specific else "Unknown",
        "city": geoip_response.city.name if geoip_response.city and geoip_response.city.name else "Unknown",
        "postal_code": geoip_response.postal.code if geoip_response.postal and geoip_response.postal.code else None,
        "latitude": geoip_response.location.latitude if geoip_response.location else None,
        "longitude": geoip_response.location.longitude if geoip_response.location else None,
    }

    # Add optional fields with defaults
    optional_fields = {
        "accuracy_radius": getattr(geoip_response.location, 'accuracy_radius', 0),
        "time_zone": getattr(geoip_response.location, 'time_zone', "Unknown"),
        "connection": {
            # Define defaults for each field within the connection dictionary
            'asn': getattr(geoip_response.traits, 'autonomous_system_number', None),
            'isp': getattr(geoip_response.traits, 'autonomous_system_organization', "Unknown"),
            'organization': getattr(geoip_response.traits, 'isp', "Unknown"),
            'domain': getattr(geoip_response.traits, 'domain', "Unknown"),
            'is_hosting_provider': getattr(geoip_response.traits, 'is_hosting_provider', False),
            'is_public_proxy': getattr(geoip_response.traits, 'is_public_proxy', False),
            'is_tor_exit_node': getattr(geoip_response.traits, 'is_tor_exit_node', False),
            'user_type': getattr(geoip_response.traits, 'user_type', "Unknown"),
        },
        "network": {
            'ip': getattr(geoip_response.traits, 'ip_address', str(ip_address)),
            'network': getattr(geoip_response.traits, 'network', None),
        }
    }
    data.update(optional_fields)

    # Pycountry and phonenumbers lookups with fallbacks
    country = pycountry.countries.get(alpha_2=geoip_response.country.iso_code) if geoip_response.country else None
    if country:
        data.update({
            "currency": getattr(pycountry.currencies.get(alpha_3=country.alpha_3), 'alpha_3', "Unknown"),
            "language": getattr(pycountry.languages.get(alpha_2=country.alpha_2), 'alpha_2', "Unknown"),
            "phone_code": phonenumbers.country_code_for_region(country.alpha_2) if country.alpha_2 else "Unknown",
        })

    return data

