"""
Django settings for myshop project.

Generated by 'django-admin startproject' using Django 4.1.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ks8qx=kt)pb2+ge)gjva06)sbnnl=p)5!()4kdtbfg^#)51vgi'


# SECURITY WARNING: don't run with debug turned on in production!
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
    'shop.apps.ShopConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
    'payment.apps.PaymentConfig',
    'coupon.apps.CouponConfig',
    'rosetta',
    'parler',
    'localflavor',
    # 'debug_toolbar',
]

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myshop.urls'

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
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'myshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en'
# PREPARING MY PROJECT FOR INTERNATIONALIZATION
LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),
]
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
# print(LOCALE_PATHS)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# django-parler settings
PARLER_LANGUAGES = {
    None: (
        {'code': 'en'},
        {'code': 'es'},
    ),
    'default': {
        'fallback': 'en',
        'hide_untranslated': False,
    }
}



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# this is for django debug toolbar
# INTERNAL_IPS = [
#     '127.0.0.1',
# ]

if DEBUG:
    import mimetypes
    mimetypes.add_type('application/javascript', '.js', True)
    mimetypes.add_type('text/css', '.css', True)


# storing shopping carts in sessions
CART_SESSION_ID = 'cart'

# Email server configuration 
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'chedjou.rocelin@gmail.com'
EMAIL_HOST_PASSWORD = 'tfefmscxjatazuff'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# if you want to send eamil to shel console 
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' 

# integration a payement method on my shop
# Stripe settings
STRIPE_PUBLISHABLE_KEY = 'pk_test_51NlrDqKWfkyyRB6guShgbDowSyOO0ecGUeM2Vc5le57LQih6IOYDelrFltl6hN0aUTiS3JUjSXkirbvRbU4H6Lw1009ONw89SM' # Publishable key
STRIPE_SECRET_KEY = 'sk_test_51NlrDqKWfkyyRB6g3RziwydrU6CDtQr8dnI9p75TgoyaV5CfbGGtEAMQZQD2LFVv0nbLlwhOQo0fndr19emkIvOs00wmkYla2g'
# Secret key
STRIPE_API_VERSION = '2023-08-16'

STRIPE_WEBHOOK_SECRET = 'whsec_fbfad550e18909c64f242b8c7dba56533ba3a599fda789d54ff2b0c099e82e62'

STATIC_ROOT = BASE_DIR / 'static'


# Redis settings
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 1


