"""
Django settings for e_commerce project.
Django 4.2.5.
"""
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta
from .utils import get_env
from .utils import get_logto_public_key

BASE_DIR = Path(__file__).resolve()

if get_env() == 'prod' or get_env() == 'production':
    dotenv_path = BASE_DIR.parent / '.env'
elif get_env() == 'stage' or get_env() == 'uat':
    dotenv_path = BASE_DIR.parent / '.env'
else:
    dotenv_path = BASE_DIR.parent / '.env'

load_dotenv(dotenv_path)

SECRET_KEY = 'xWA2U0dJt7c9SJgGXyoqlbhzirsaaeE1fkIOdIP6-yoWKk-95lljC_LAr8eL3n_qAbk'

DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework',
    'rest_framework_simplejwt'
]

# Third Party
INSTALLED_APPS += [
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',

    'dynamic_preferences',
    'dynamic_preferences.users.apps.UserPreferencesConfig',
    'storages',
]

# Documentation
INSTALLED_APPS += [
    'drf_spectacular',
    'django_filters',
]

# Our Apps
INSTALLED_APPS += [
    'setup',
    'users',
    'masterdata',
    'product',
    'inventory',
    'customer',
    'orders',
    'transaction',
    'cms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'setup.middleware.request.CurrentRequestMiddleware',
]

ROOT_URLCONF = 'e_commerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'dynamic_preferences.processors.global_preferences',
            ],
        },
    },
]

WSGI_APPLICATION = 'e_commerce.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR.parent / 'staticfiles'

# MEDIA
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(BASE_DIR.parent / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "users.authentication.LogtoJWTAuthentication",
        # "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    "DEFAULT_PAGINATION_CLASS": "setup.pagination.CustomPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": 'drf_spectacular.openapi.AutoSchema',
    "DATETIME_FORMAT": "%Y-%m-%d %I:%M %p",
    "AUTHENTICATION_EXTENSIONS": "rest_framework_simplejwt.authentication.LogtoJWTAuthenticationExtension",
    "DEFAULT_AUTHENTICATION_CLASSES_FOR_SCHEMA": "users.authentication.NoOpAuthentication"
}

SPECTACULAR_SETTINGS = {
    "TITLE": "SignUp API",
    "DESCRIPTION": "Documentation of API endpoints of SignUp APP",
    "VERSION": "1.0.0",
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    'SERVE_AUTHENTICATION': ["rest_framework.authentication.SessionAuthentication"],
    "AUTHENTICATION_WHITELIST": None,
    "SERVE_INCLUDE_SCHEMA": True,
    "COMPONENT_SPLIT_REQUEST": True,
    "SECURITY": [{"bearerAuth": []}],
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
    },
    'SWAGGER_UI_DIST': 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest',
    'SWAGGER_UI_FAVICON_HREF': 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/favicon-32x32.png',
    'REDOC_DIST': 'https://cdn.jsdelivr.net/npm/redoc@latest',
    'TAGS': [
        {'name': 'Setup', 'description': 'Endpoints for setup and configuration'},
        {'name': 'LOG TO', 'description': 'Endpoints for Log-to authentication'},
        {'name': 'Account', 'description': 'User account management'},
        {'name': 'Master Data', 'description': 'Endpoints for managing master data'},
        {'name': 'Inventory', 'description': 'Inventory management'},
        {'name': 'Products', 'description': 'Product-related endpoints'},
        {'name': 'Customer', 'description': 'Customer-related operations'},
        {'name': 'Orders', 'description': 'Order management'},
        {'name': 'Transaction', 'description': 'Transaction processing'},
        {'name': 'CMS', 'description': 'Content management system'},
        {'name': 'Home', 'description': 'General endpoints for home or dashboard'},
    ],
}

LOGTO_APP_ID = os.environ.get('LOGTO_APP_ID')
LOGTO_APP_SECRET = os.environ.get('LOGTO_APP_SECRET')
LOGTO_MANAGEMENT_ENDPOINT = os.environ.get('LOGTO_MANAGEMENT_ENDPOINT')
LOGTO_M2M_RESOURCE = os.environ.get('LOGTO_M2M_RESOURCE')
LOGTO_TOKEN_URL = os.environ.get('LOGTO_M2M_RESOURCE')
LOGTO_ISSUER = os.environ.get('LOGTO_ISSUER')
LOGTO_AUDIENCE = os.environ.get('LOGTO_AUDIENCE')
LOGTO_CERTS_URL = os.environ.get('LOGTO_CERTS_URL')

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),

    "ALGORITHM": "ES384",
    "USER_ID_CLAIM": "sub",
    "USER_ID_FIELD": "sub",

    "AUTH_HEADER_TYPES": ("Bearer",),
}

# available settings with their default values
DYNAMIC_PREFERENCES = {

    # a python attribute that will be added to model instances with preferences
    # override this if the default collide with one of your models attributes/fields
    'MANAGER_ATTRIBUTE': 'preferences',

    # The python module in which registered preferences will be searched within each app
    'REGISTRY_MODULE': 'dynamic_preferences_registry',

    # Allow quick editing of preferences directly in admin list view
    # WARNING: enabling this feature can cause data corruption if multiple users
    # use the same list view at the same time, see https://code.djangoproject.com/ticket/11313
    'ADMIN_ENABLE_CHANGELIST_FORM': False,

    # Customize how you can access preferences from managers. The default is to
    # separate sections and keys with two underscores. This is probably not a settings you'll
    # want to change, but it's here just in case
    'SECTION_KEY_SEPARATOR': '__',

    # Use this to disable auto registration of the GlobalPreferenceModel.
    # This can be useful to register your own model in the global_preferences_registry.
    'ENABLE_GLOBAL_MODEL_AUTO_REGISTRATION': True,

    # Use this to disable caching of preference. This can be useful to debug things
    'ENABLE_CACHE': True,

    # Use this to select which chache should be used to cache preferences. Defaults to default.
    'CACHE_NAME': 'default',

    # Use this to disable checking preferences names. This can be useful to debug things
    'VALIDATE_NAMES': True,
}

SITE_ID = 1

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = 3000
SESSION_COOKIE_AGE = 3000
SESSION_SAVE_EVERY_REQUEST = True

CORS_ORIGIN_ALLOW_ALL = True

CORS_URLS_REGEX = r"^/api/.*$"

# ALGOLIA = {
#     'APPLICATION_ID': '6U8MXHFLJW',
#     'API_KEY': '9335c56e84ceac681c30904edcff4dae',
# }

CSRF_TRUSTED_ORIGINS = [
    'https://manage.signupcasuals.com/',
]

URL_PREFIX = ''

DATE_FORMAT = ['%Y-%m-%d', '%d-%m-%Y']

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID') 
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY') 
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')  
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_QUERYSTRING_AUTH = True # Optional: Makes media URLs public without signed URLs

# Static files storage
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Media files storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS_LOCATION = 'media'  # E.g., "media" or "static"
AWS_S3_FILE_OVERWRITE = False  # To prevent overwriting files with the same name

SHIP_ROCKET_EMAIL = os.getenv('SHIP_ROCKET_EMAIL')
SHIP_ROCKET_PASSWORD = os.getenv('SHIP_ROCKET_PASSWORD')
