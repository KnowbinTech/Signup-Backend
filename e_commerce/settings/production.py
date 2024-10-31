from .base import *

DEBUG = True

INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS

ALLOWED_HOSTS = [
    "localhost:3000",
    "https://backend.signupcasuals.com",
    "https://backend.signupcasuals.com",
    "backend.signupcasuals.com",
     "localhost",
    "0.0.0.0",
    "127.0.0.1",
    "manage.signupcasuals.com",
    "signupcasuals.com",
    "signupbackend.knowbin.tech",
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    "https://backend.signupcasuals.com",
     "https://backend.signupcasuals.com",
    "backend.signupcasuals.com",
     "https://localhost",
    "https://0.0.0.0",
    "https://127.0.0.1",
    'http://manage.signupcasuals.com',
    'https://manage.signupcasuals.com',
    'http://signupcasuals.com',
    'https://signupcasuals.com',
    'https://signupbackend.knowbin.tech',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    "https://backend.signupcasuals.com",
     "https://backend.signupcasuals.com",
    "backend.signupcasuals.com",
   "https://localhost",
    "https://0.0.0.0",
    "https://127.0.0.1",
    'https://manage.signupcasuals.com:8443',
    'https://manage.signupcasuals.com',
    'https://signupcasuals.com',
    'https://signupbackend.knowbin.tech:8001',
    'https://signupbackend.knowbin.tech',
]

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    "https://backend.signupcasuals.com",
     "https://backend.signupcasuals.com",
    "backend.signupcasuals.com",
     "localhost",
    "0.0.0.0",
    "127.0.0.1",
    'https://manage.signupcasuals.com:8443',
    'https://manage.signupcasuals.com',
    'https://signupcasuals.com',
    'https://signupbackend.knowbin.tech:8001',
    'https://signupbackend.knowbin.tech',
]

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
# SECURE_SSL_REDIRECT = False

# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
# SECURE_CONTENT_TYPE_NOSNIFF = False

# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_REFERRER_POLICY = None

# X_FRAME_OPTIONS = 'DENY'

CSRF_COOKIE_NAME = 'csrftoken'
# Set the CSRF cookie domain
CSRF_COOKIE_DOMAIN = [
     "https://backend.signupcasuals.com",
    "backend.signupcasuals.com",
    'https://manage.signupcasuals.com:8443',
    "https://backend.signupcasuals.com",
    'https://manage.signupcasuals.com',
    'https://signupcasuals.com',
    'https://signupbackend.knowbin.tech:8001',
    'https://signupbackend.knowbin.tech',
     "localhost",
    "0.0.0.0",
    "127.0.0.1",
]

# Set the secure flag for the CSRF cookie (recommended for HTTPS)
CSRF_COOKIE_SECURE = True

# Set the path for the CSRF cookie
CSRF_COOKIE_PATH = '/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'signupdb',
        'USER': 'signupadmin',
        'PASSWORD': 'HelloSignup789',
        'HOST': 'w08ww8gsw0g4w0ggo4g8kkkc',
        'PORT': '5432',
    }
}

STATICFILES_DIRS = [os.path.join(BASE_DIR.parent, 'static')]
STATIC_ROOT = BASE_DIR.parent / 'staticfiles'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '143621340002-lmgf8f4tb5i5blkdt3hptkb5fsk6930m.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'
# SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = 'http://127.0.0.1:8000/accounts/google/login/callback/'
# LOGIN_REDIRECT_URL = 'http://127.0.0.1:8000/accounts/google/login/callback/'
# LOGOUT_REDIRECT_URL = 'http://127.0.0.1:8000/accounts/google/login/callback/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.knowbintech.com'
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

USER_ID = os.environ.get('PHONE_PE_USER_ID')
MERCHANT_KEY = os.environ.get('PHONE_PE_MERCHANT_ID')
API_KEY = os.environ.get('PHONE_PE_API_KEY')
KEY_INDEX = os.environ.get('PHONE_PE_KEY_INDEX')

PHONE_PAY_S2S_CALLBACK_URL = os.environ.get('PHONE_PAY_S2S_CALLBACK_URL')
PHONE_PAY_REDIRECT_URL = os.environ.get('PHONE_PAY_REDIRECT_URL')
