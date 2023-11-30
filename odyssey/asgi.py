"""
ASGI config for odyssey project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import django

from dotenv import load_dotenv

load_dotenv()

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'odyssey.settings.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'odyssey.settings.{os.environ.get("SETTINGS")}')
django.setup()
application = get_asgi_application()
