from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from urllib.parse import urlparse
from rest_framework import serializers


class DomainSerializer(serializers.Serializer):
    domains = serializers.ListField(
        child=serializers.CharField(max_length=100)
    )

    def validate_domains(self, domains):
        validated_domains = []
        for domain in domains:
            clean_domain = self.validate_and_clean_domain(domain)
            if clean_domain:
                validated_domains.append(clean_domain)
        return validated_domains

    @staticmethod
    def validate_and_clean_domain(domain):
        if not domain:
            raise serializers.ValidationError("Empty domain name provided.")

        # Remove http/https and www prefixes
        if domain.startswith(('http://', 'https://')):
            parsed_domain = urlparse(domain).netloc
        else:
            parsed_domain = domain

        parsed_domain = parsed_domain.split('www.')[-1]  # Remove www

        # Validate domain format
        url_validator = URLValidator()
        try:
            url_validator('http://' + parsed_domain)
        except ValidationError:
            raise serializers.ValidationError(f"Invalid domain format: {domain}")

        return parsed_domain


class DomainDetailSerializer(serializers.Serializer):
    domain = serializers.CharField(max_length=100)

    def validate_domain(self, domain):
        return DomainSerializer.validate_and_clean_domain(domain)


class DomainSuggestionSerializer(serializers.Serializer):
    domain = serializers.CharField(max_length=100)
