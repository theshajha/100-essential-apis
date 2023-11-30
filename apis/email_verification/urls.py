from django.urls import path
from .views import VerifyEmailView

app_name = 'email_verification'

urlpatterns = [
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
]
