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
        ip_list = x_forwarded_for.split(',')
        client_ip = ip_list[0].strip()
    else:
        client_ip = request.META.get('REMOTE_ADDR')
    return client_ip, True


@throttle_classes([AnonRateThrottle])
@permission_classes((permissions.AllowAny,))
class IPGeocodeView(APIView):

    def get(self, request, ip_address=None, format=None):
        # Use a settings variable for the path to the GeoLite2-City database
        geo_db_path = getattr(settings, 'GEOLITE2_CITY_DB_PATH', 'path/to/GeoLite2-City.mmdb')
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
            reader.close()
            return Response({"error": "IP address not found"}, status=404)
        except Exception as e:
            reader.close()
            capture_exception(e)
            return Response({"error": "An error occurred while processing the IP address."}, status=500)

        data = build_geoip_data(response, ip_address)

        # Save the data in cache for future requests
        timeout = getattr(settings, 'GEOIP_CACHE_TIMEOUT', 86400)  # Default to 24 hours
        cache.set(cache_key, data, timeout=timeout)

        reader.close()

        return Response(data)


def build_geoip_data(geoip_response, ip_address):
    data = {
        "ip": ip_address,
        "country_code": geoip_response.country.iso_code,
        "country_name": geoip_response.country.name,
        "region_code": geoip_response.subdivisions.most_specific.iso_code,
        "region_name": geoip_response.subdivisions.most_specific.name,
        "city": geoip_response.city.name,
        "postal_code": geoip_response.postal.code,
        "latitude": geoip_response.location.latitude,
        "longitude": geoip_response.location.longitude,
    }

    # Add optional fields
    optional_fields = {
        "accuracy_radius": geoip_response.location.accuracy_radius,
        "time_zone": geoip_response.location.time_zone,
        "connection": {
            'asn': geoip_response.traits.autonomous_system_number,
            'isp': geoip_response.traits.autonomous_system_organization,
            'organization': geoip_response.traits.isp,
            'domain': geoip_response.traits.domain,
            'is_hosting_provider': geoip_response.traits.is_hosting_provider,
            'is_public_proxy': geoip_response.traits.is_public_proxy,
            'is_tor_exit_node': geoip_response.traits.is_tor_exit_node,
            'user_type': geoip_response.traits.user_type,
        },
        "network": {
            'ip': geoip_response.traits.ip_address,
            'network': geoip_response.traits.network,
        }
    }
    for key, value in optional_fields.items():
        if value:
            data[key] = value

    # Pycountry and phonenumbers lookups
    country = pycountry.countries.get(alpha_2=geoip_response.country.iso_code)
    if country:
        data.update({
            "currency": getattr(pycountry.currencies.get(alpha_3=country.alpha_3), 'alpha_3', None),
            "language": getattr(pycountry.languages.get(alpha_2=country.alpha_2), 'alpha_2', None),
            "phone_code": phonenumbers.country_code_for_region(country.alpha_2)
        })

    return data

