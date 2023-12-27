from .throttles import CustomScopedRateThrottle

from rest_framework.permissions import BasePermission

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import whois
import tldextract
import itertools
from .serilaizers import *


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        # Implement custom permission logic
        return True


class BaseDomainAPIView(APIView):
    throttle_classes = [CustomScopedRateThrottle]
    permission_classes = [CustomPermission]

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        custom_response = {
            'error': 'An unexpected error occurred',
            'details': str(exc)
        }
        response.data = custom_response
        return response

    def success_response(self, data):
        return Response(data, status=status.HTTP_200_OK)

    def error_response(self, errors, http_status=status.HTTP_400_BAD_REQUEST):
        return Response(errors, status=http_status)


class DomainStatusView(BaseDomainAPIView):
    def post(self, request, *args, **kwargs):
        serializer = DomainSerializer(data=request.data)
        if serializer.is_valid():
            domains = serializer.validated_data['domains']
            results = [{domain: self.get_domain_status(domain)} for domain in domains]
            return self.success_response(results)
        return self.error_response(serializer.errors)

    @staticmethod
    def get_domain_status(domain):
        try:
            w = whois.whois(domain)
            return "Registered" if w.domain_name else "Available"
        except Exception as e:
            return str(e)


class DomainDetailView(BaseDomainAPIView):
    def post(self, request, *args, **kwargs):
        serializer = DomainDetailSerializer(data=request.data)
        if serializer.is_valid():
            domain = serializer.validated_data['domain']
            try:
                w = whois.whois(domain)
                return self.success_response(w)
            except Exception as e:
                return self.error_response({'error': str(e)})
        return self.error_response(serializer.errors)


class DomainSuggestionView(BaseDomainAPIView):
    def post(self, request, *args, **kwargs):
        serializer = DomainSuggestionSerializer(data=request.data)
        if serializer.is_valid():
            domain = serializer.validated_data['domain']
            suggestions = self.generate_domain_suggestions(domain)
            statuses = {suggestion: self.get_domain_status(suggestion) for suggestion in suggestions}
            return self.success_response(statuses)
        return self.error_response(serializer.errors)

    def generate_domain_suggestions(self, domain):
        extracted = tldextract.extract(domain)
        base_domain = extracted.domain

        # List of popular TLDs and SLDs
        popular_tlds = ["com", "net", "org", "io", "co"]
        popular_slds = ["", "get", "my", "app", "online"]

        # Generate domain variations
        variations = set()
        for sld, tld in itertools.product(popular_slds, popular_tlds):
            if sld:
                variation = f"{sld}{base_domain}.{tld}"
            else:
                variation = f"{base_domain}.{tld}"
            if variation != domain:  # Exclude the original domain
                variations.add(variation)

        return list(variations)

    @staticmethod
    def get_domain_status(domain):
        try:
            w = whois.whois(domain)
            return "Available" if not w.domain_name else "Unavailable"
        except Exception as e:
            return str(e)
