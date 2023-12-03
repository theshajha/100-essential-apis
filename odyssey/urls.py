"""odyssey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *
from django.contrib.staticfiles.views import serve as serve_static
admin.site.site_header = 'Tiny API Admin'


def _static_butler(request, path, **kwargs):
    """
    Serve static files using the django static files configuration
    WITHOUT collectstatic. This is slower, but very useful for API
    only servers where the static files are really just for /admin

    Passing insecure=True allows serve_static to process, and ignores
    the DEBUG=False setting
    """
    return serve_static(request, path, insecure=True, **kwargs)


router = DefaultRouter()

# TODO: add path for password reset - https://dev.to/earthcomfy/django-reset-password-3k0l

urlpatterns = [
                  path('v1/', include('apis.urls', '100_essential_apis'), name='100_essential_apis'),
                  path('health/', HealthCheck.as_view(), name='health_check_api'),
              ] + router.urls

urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
