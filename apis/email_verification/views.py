from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import re
import dns.resolver
import smtplib

from .throttles import CustomScopedRateThrottle

from rest_framework.permissions import BasePermission


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        # Implement custom permission logic
        return True


class VerifyEmailView(APIView):
    throttle_classes = [CustomScopedRateThrottle]
    permission_classes = [CustomPermission]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        if not email:
            return Response({'detail': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not self.is_valid_email_format(email):
            return Response({'detail': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)

        if not self.is_valid_domain(email):
            return Response({'detail': 'Invalid domain'}, status=status.HTTP_400_BAD_REQUEST)

        exists = self.check_email_existence(email)
        return Response({'email': email, 'exists': exists}, status=status.HTTP_200_OK)

    @staticmethod
    def is_valid_email_format(email):
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email)

    @staticmethod
    def is_valid_domain(email):
        domain = email.split('@')[-1]

        try:
            dns.resolver.resolve(domain, 'MX')
            return True
        except dns.resolver.NXDOMAIN:
            return False
        except dns.resolver.NoAnswer:
            return False
        except dns.resolver.Timeout:
            return False

    @staticmethod
    def check_email_existence(email):
        domain = email.split('@')[-1]
        try:
            records = dns.resolver.resolve(domain, 'MX')
            mx_record = records[0].exchange.to_text().rstrip('.')

            server = smtplib.SMTP(timeout=10)
            server.set_debuglevel(0)
            server.connect(mx_record)
            server.helo(server.local_hostname)
            server.mail('')
            code, _ = server.rcpt(email)
            server.quit()

            return code == 250
        except (dns.resolver.NXDOMAIN, smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError):
            return False
        except dns.resolver.NoAnswer:
            return False
        except dns.resolver.Timeout:
            return False
