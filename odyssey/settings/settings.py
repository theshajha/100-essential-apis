from .common import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://27571adf76374092a59e79ecf7ef0be2@o288960.ingest.sentry.io/4504978956615680",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0.5,
    environment="odyssey",

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,

    _experiments={
        "profiles_sample_rate": 1.0,
    },
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'odyssey_web', '52.21.42.218', 'http://odyssey.tinyapi.co', 'https://odyssey.tinyapi.co',
                 'odyssey.tinyapi.co']

# ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'dddb.sqlite3',
#     }
# }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# WHITENOISE STATIC SETUP
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_HOST = "https://dsb9x7s4sz67o.cloudfront.net" if not DEBUG else ""
STATIC_URL = STATIC_HOST + "/static/"

SIMPLE_JWT = {
    # 'ACCESS_TOKEN_LIFETIME': timedelta(minutes=2),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
    'SIGNING_KEY': SECRET_KEY,
}

BASE_APP_URL = 'https://staging.odyssey.co'
BASE_API_URL = 'http://localhost:8002'
