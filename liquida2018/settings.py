# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from unittest.mock import DEFAULT
import django_heroku
from django.urls import reverse_lazy
# import psycopg2
#
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#
# DATABASE_URL = os.environ['DATABASE_URL']
#
# conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-ocvjf&p1d%!))e)dpp_uu39s-+=)w&!*oc$vl48o@n*_1fh%2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Teste
ALLOWED_HOSTS = ['127.0.0.1', 'www.sorteioapadpisocial.com.br', '.sorteioapadpisocial.com.br']
# ALLOWED_HOSTS = ['127.0.0.1', 'https://apad-a3824e4005be.herokuapp.com/', '.apad-a3824e4005be.herokuapp.com/']
# ALLOWED_HOSTS = ['*']

# SECURE_SSL_REDIRECT = True

# Ajuda a abrir cupons na no firefox Importante
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'ALLOW-FROM https://apad-a3824e4005be.herokuapp.com/'


# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATE_INPUT_FORMATS = ['%d-%m-%Y']

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Application definition

INSTALLED_APPS = (
    'bcp',
    'cupom',
    'participante',
    'lojista',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'django_filters',
    'bootstrap4',
    'sorl.thumbnail',
    # 'djng',
    'storages',
    'import_export',
    'logentry_admin',
    'parsley',
    'anymail',
)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'liquida2018.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'liquida2018.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Este é o banco oficial

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'apad-backup',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',

    }
}

# Testes

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'liquidateresina2018',
#         'USER': 'liquida2018',
#         'PASSWORD': 'solution',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

AWS_ACCESS_KEY_ID = 'AKIASJX2S5JMTWNNNJHQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'liquida2023'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_LOCATION_QRCODES = 'qrcodes'



AWS_LOCATION = 'static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

DEFAULT_FILE_STORAGE = 'liquida2018.storage_backends.MediaStorage'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
# STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static'),]
#
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'tmp')

# FORM_RENDERER = 'djng.forms.renderers.DjangoAngularBootstrap3Templates'
# FORM_RENDERER = 'djng.forms.renderers.DjangoAngularTemplates'




# LOGIN_REDIRECT_URL = reverse_lazy('participante:dashboard')
# settings.py

# LOGIN_REDIRECT_URL = 'participante:dashboard'
# LOGIN_URL = reverse_lazy('participante:login')
# LOGOUT_URL = reverse_lazy('participante:logout')

# LOGIN_REDIRECT_URL = "home"
# LOGOUT_REDIRECT_URL = "home"

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('participante:editdocfiscal', args=[u.nomedocumento])
}

# ANYMAIL = {
#     # (exact settings here depend on your ESP...)
#     "MAILGUN_API_KEY": "2fe56e35487ac43118a55396cd8ab5d3-5e7fba0f-93b3040e",
#     "MAILGUN_SENDER_DOMAIN": 'liquida2022.com.br',  # your Mailgun domain, if needed
# }
# # EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"  # or sendgrid.EmailBackend, or...
# DEFAULT_FROM_EMAIL = "liquida2021@liquida2021.com.br"  # if you don't already have this in settings
# SERVER_EMAIL = "liquida2022.com.br"  # ditto (default from-email for Django errors)

# EMAIL_SUBJECT_PREFIX = 'Liquida 2022'
# EMAIL_HOST = 'smtp.mailgun.org'
# EMAIL_HOST_USER = 'suporte@liquida2022.com.br'
# EMAIL_HOST_PASSWORD = '6f9efe4b6c271d81d3931b44ac2fa12a-9776af14-befba8d1'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True



EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
DEFAULT_FROM_EMAIL = 'suporte@mg.liquidateresina.com.br'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

ANYMAIL = {
    'MAILGUN_API_KEY' : '2fe56e35487ac43118a55396cd8ab5d3-5e7fba0f-93b3040e',
    'MAILGUN_SENDER_DOMAIL' :'mg.liquidateresina.com.br'
}


# python-social-auth settings
AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.Facebook2OAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',

    'django.contrib.auth.backends.ModelBackend',
    'participante.authentication.EmailAuthBackend',
)

SOCIAL_AUTH_FACEBOOK_KEY = '340442496482403'
SOCIAL_AUTH_FACEBOOK_SECRET = '8c550fd5dd91ec4ebce457a00afea8ea'

SOCIAL_AUTH_TWITTER_KEY = ''
SOCIAL_AUTH_TWITTER_SECRET = ''

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

# import dj_database_url
# DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

DEBUG_PROPAGATE_EXCEPTIONS = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# QR_CODE_DIR = os.path.join(BASE_DIR, 'qrcode')

django_heroku.settings(locals())



