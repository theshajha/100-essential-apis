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

# from ipware import get_client_ip


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_list = x_forwarded_for.split(',')
        client_ip = ip_list[0].strip()
    else:
        client_ip = request.META.get('REMOTE_ADDR')
    return client_ip, True


class IPGeocodeSerializer(serializers.Serializer):
    ip = serializers.CharField()
    country_code = serializers.CharField()
    country_name = serializers.CharField()
    region_code = serializers.CharField()
    region_name = serializers.CharField()
    city = serializers.CharField()
    postal_code = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    currency = serializers.CharField()


@throttle_classes([AnonRateThrottle])
@permission_classes((permissions.AllowAny,))
class IPGeocodeView(APIView):
    # @log_api_request
    def get(self, request, ip_address=None, format=None):
        # Replace 'path/to/GeoLite2-City.mmdb' with the actual path to the downloaded database
        reader = Reader('apis/ip_geocode/GeoLite2-City.mmdb')

        if not ip_address:
            if request is None:
                return Response(
                    {'error': 'Request object is required when IP is not provided', 'ip_address': ip_address},
                    status=400)

            client_ip, is_routable = get_client_ip(request)
            if client_ip is None:
                return Response({'error': 'Unable to determine IP address', 'ip_address': ip_address}, status=400)
            else:
                # Got the client's IP address
                if is_routable:
                    # The client's IP address is a public IP
                    ip_address = client_ip
                else:
                    # The client's IP address is a private IP
                    return Response(
                        {'error': 'Geolocation data not available for private IP addresses', 'ip_address': ip_address},
                        status=400)

        try:
            response = reader.city(ip_address)
        except AddressNotFoundError:
            return Response({"error": "IP address not found", 'ip_address': ip_address}, status=404)

        country = pycountry.countries.get(alpha_2=response.country.iso_code)
        subdivision = response.subdivisions.most_specific

        data = {
            "ip": ip_address,
            "country_code": response.country.iso_code,
            "country_name": response.country.name,
            "region_code": subdivision.iso_code,
            "region_name": subdivision.name,
            "city": response.city.name,
            "postal_code": response.postal.code,
            "latitude": response.location.latitude,
            "longitude": response.location.longitude,
        }

        if response.location.accuracy_radius:
            data["accuracy_radius"] = response.location.accuracy_radius

        if response.location.time_zone:
            data["time_zone"] = response.location.time_zone

        if country:
            try:
                currency = pycountry.currencies.get(alpha_3=response.country.iso_code)
                if currency:
                    data["currency"] = currency.alpha_3

                language = pycountry.languages.get(alpha_2=country.alpha_2)
                if language:
                    data["language"] = language.alpha_2

            except Exception as e:
                capture_exception(e)
                pass

            try:
                phone_code = phonenumbers.country_code_for_region(country.alpha_2)
                data["phone_code"] = f"+{phone_code}"
            except Exception as e:
                capture_exception(e)
                pass

        if response.traits:
            traits = json.dumps(response.traits.__dict__)
            json_traits = json.loads(traits)
            try:
                data["connection"] = {
                    'asn': json_traits['autonomous_system_number'],
                    'isp': json_traits['autonomous_system_organization'],
                    'organization': json_traits['isp'],
                    'domain': json_traits['domain'],
                    'is_hosting_provider': json_traits['is_hosting_provider'],
                    'is_public_proxy': json_traits['is_public_proxy'],
                    'is_tor_exit_node': json_traits['is_tor_exit_node'],
                    'user_type': json_traits['user_type'],
                }
            except Exception as e:
                capture_exception(e)
                pass

            try:
                data["security"] = {
                    'is_proxy': json_traits['is_anonymous_proxy'],
                    'is_crawler': json_traits['is_anonymous'],
                    'proxy_type': None,  # Need to use a third-party API or package to determine the proxy type
                    'crawler_name': None  # Need to use a third-party API or package to determine the crawler name
                }
            except Exception as e:
                capture_exception(e)
                pass

            try:
                data["network"] = {
                    'ip': json_traits['ip_address'],
                    'network': json_traits['network'],
                    'network_type': json_traits['network_type'],
                }
            except Exception as e:
                capture_exception(e)
                pass

        reader.close()

        return Response(data)
