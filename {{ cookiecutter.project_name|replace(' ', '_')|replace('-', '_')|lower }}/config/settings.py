import datetime
import secrets
import sys

import environ
import raven
from django.conf.global_settings import LANGUAGES as BASE_LANGUAGES
from django.contrib import messages
{%- if cookiecutter.use_celery == "y" and cookiecutter.use_rabbitmq == "y" %}
from kombu import Queue, Exchange
{%- endif %}
from model_utils import Choices

from .logging import LOGGING

ROOT_DIR = environ.Path(__file__) - 2
APPS_DIR = ROOT_DIR.path('project')

sys.path.append(APPS_DIR.path('apps').root)

##############################################################################
# Default values for variables which should be present in .env file
##############################################################################

env = environ.Env(

    DJANGO_DEBUG=(bool, False),
    DJANGO_DEBUG_PROPAGATE_EXCEPTIONS=(bool, False),

    DJANGO_CSRF_USE_SESSIONS=(bool, True),
    DJANGO_SECRET_KEY=(str, secrets.token_urlsafe(50)),

    DJANGO_DATABASE_URL=(str, 'sqlite://'),

    DJANGO_CACHE=(str, 'locmemcache://'),

    DJANGO_ALLOWED_HOSTS=(list, []),
    DJANGO_DISALLOWED_USER_AGENTS=(list, []),
    DJANGO_INTERNAL_IPS=(list, []),
    DJANGO_DEFAULT_HTTP_PROTOCOL=(str, 'http'),

    DJANGO_ADMIN_URL=(str, 'admin/'),

    DJANGO_ADMINS=(list, []),
    DJANGO_DEFAULT_FROM_EMAIL=(str, 'webmaster@localhost'),
    DJANGO_SERVER_EMAIL=(str, 'root@localhost'),
    DJANGO_EMAIL_URL=(str, 'consolemail://'),
    DJANGO_EMAIL_USE_LOCALTIME=(bool, True),
    DJANGO_EMAIL_SUBJECT_PREFIX=(str, 'Django'),
    DJANGO_EMAIL_SSL_CERTFILE=(str, ''),
    DJANGO_EMAIL_SSL_KEYFILE=(str, ''),

    DJANGO_DEFAULT_FILE_STORAGE=(str, 'django.core.files.storage.FileSystemStorage'),
    DJANGO_STATIC_ROOT=(str, str(APPS_DIR.path('staticfiles').root)),
    DJANGO_MEDIA_ROOT=(str, str(APPS_DIR.path('media').root)),

    {%- if cookiecutter.use_cors == "y" %}
    CORS_ORIGIN_WHITELIST=(list, []),
    {%- endif %}

    {%- if cookiecutter.use_allauth == "y" %}
    ALLAUTH_USERNAME_BLACKLIST=(list, []),
    ALLAUTH_CONFIRMATION_EXPIRE_DAYS=(int, 3),
    ALLAUTH_LOGIN_ATTEMPTS_LIMIT=(int, 5),
    ALLAUTH_LOGIN_ATTEMPTS_TIMEOUT=(int, 300),
    {%- endif %}

    {%- if cookiecutter.use_rest == "y" %}
    JWT_SECRET_KEY=(str, secrets.token_urlsafe(50)),
    JWT_EXPIRATION_DELTA=(int, 300),
    JWT_REFRESH_EXPIRATION_DELTA=(int, 604800),
    {%- endif %}


    DJANGO_USE_DEBUG_TOOLBAR=(bool, False),
    DJANGO_DEBUG_SQL=(bool, False),
    DJANGO_DEBUG_SQL_COLOR=(bool, False),

    DJANGO_USE_SILK=(bool, False),
    DJANGO_SENTRY_DSN=(str, ''),

    {%- if cookiecutter.use_celery == "y" %}
    CELERY_ALWAYS_EAGER=(bool, False),
    CELERY_RESULT_BACKEND=(str, 'django-db'),
    CELERY_BROKER_URL=(str, 'amqp://'),
    CELERY_IGNORE_RESULT=(bool, True),
    {%- endif %}
)

environ.Env.read_env()

##############################################################################
# Debugging
# https://docs.djangoproject.com/en/2.0/ref/settings/#debugging
##############################################################################

DEBUG = env.bool('DJANGO_DEBUG')

DEBUG_PROPAGATE_EXCEPTIONS = env.bool('DJANGO_DEBUG_PROPAGATE_EXCEPTIONS')

##############################################################################
# Security
# https://docs.djangoproject.com/en/2.0/ref/settings/#security
##############################################################################

CSRF_USE_SESSIONS = env.bool('DJANGO_CSRF_USE_SESSIONS')

SECRET_KEY = env.str('DJANGO_SECRET_KEY')

##############################################################################
# Sites
# https://docs.djangoproject.com/en/2.0/ref/settings/#sites
##############################################################################

SITE_ID = 1

##############################################################################
# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#database
##############################################################################

DATABASES = {
    'default': env.db('DJANGO_DATABASE_URL')
}

##############################################################################
# Cache
# https://docs.djangoproject.com/en/2.0/ref/settings/#cache
##############################################################################

CACHES = {
    'default': env.cache_url('DJANGO_CACHE')
}

##############################################################################
# Models
# https://docs.djangoproject.com/en/2.0/ref/settings/#models
##############################################################################

ABSOLUTE_URL_OVERRIDES = {}

FIXTURE_DIRS = []

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
)

THIRD_PARTY_APPS = (
    'django_extensions',
{%- if cookiecutter.use_allauth == 'y' %}
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
{%- endif %}
{%- if cookiecutter.use_allauth == 'y' and cookiecutter.use_rest == 'y' %}
    'rest_auth',
    'rest_auth.registration',
{%- endif %}
{%- if cookiecutter.use_rest == 'y' %}
    'rest_framework',
{%- endif %}
{%- if cookiecutter.use_constance == 'y' %}
    'constance',
    'constance.backends.database',
{%- endif %}
{%- if cookiecutter.use_cors == 'y' %}
    'corsheaders',
{%- endif %}
{%- if cookiecutter.use_celery == 'y' %}
    'django_celery_results',
{%- endif %}
)

LOCAL_APPS = (
    'common.apps.CommonConfig',
    'users.apps.UsersConfig',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

##############################################################################
# HTTP
# https://docs.djangoproject.com/en/2.0/ref/settings/#http
##############################################################################

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

DEFAULT_HTTP_PROTOCOL = env.str('DJANGO_DEFAULT_HTTP_PROTOCOL')

MIDDLEWARE = (
{%- if cookiecutter.use_cors == 'y' %}
    'corsheaders.middleware.CorsMiddleware',
{%- endif %}
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# https://docs.djangoproject.com/en/2.0/ref/settings/#data-upload-max-memory-size
DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5 MB

# https://docs.djangoproject.com/en/2.0/ref/settings/#data-upload-max-number-fields
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

DISALLOWED_USER_AGENTS = env.list('DJANGO_DISALLOWED_USER_AGENTS')

INTERNAL_IPS = ('127.0.0.1', '0.0.0.0', '10.0.2.2') if DEBUG else env.list('DJANGO_INTERNAL_IPS')

WSGI_APPLICATION = 'config.wsgi.application'

##############################################################################
# URLs
# https://docs.djangoproject.com/en/2.0/ref/settings/#urls
##############################################################################

ADMIN_URL = env.str('DJANGO_ADMIN_URL')

APPEND_SLASH = True

PREPEND_WWW = False

ROOT_URLCONF = 'config.urls'

##############################################################################
# Auth
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth
##############################################################################

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    {%- if cookiecutter.use_allauth == 'y' %}
    'allauth.account.auth_backends.AuthenticationBackend',
    {%- endif %}
)

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

##############################################################################
# Email
# https://docs.djangoproject.com/en/2.0/ref/settings/#email
##############################################################################

ADMINS = [tuple(admins.split(':')) for admins in env.list('DJANGO_ADMINS')]

MANAGERS = ADMINS

DEFAULT_FROM_EMAIL = env.str('DJANGO_DEFAULT_FROM_EMAIL')

SERVER_EMAIL = env.str('DJANGO_SERVER_EMAIL')

EMAIL_URL = env.email_url('DJANGO_EMAIL_URL')

EMAIL_BACKEND = EMAIL_URL.get('EMAIL_BACKEND')

EMAIL_FILE_PATH = env.str('EMAIL_FILE_PATH', APPS_DIR.path('media/email').root)

EMAIL_HOST = EMAIL_URL.get('EMAIL_HOST')

EMAIL_PORT = EMAIL_URL.get('EMAIL_PORT')

EMAIL_HOST_USER = EMAIL_URL.get('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = EMAIL_URL.get('EMAIL_HOST_PASSWORD')

EMAIL_USE_TLS = EMAIL_URL.get('EMAIL_USE_TLS')

EMAIL_USE_SSL = EMAIL_URL.get('EMAIL_USE_SSL')

EMAIL_USE_LOCALTIME = env.bool('DJANGO_EMAIL_USE_LOCALTIME')

EMAIL_SUBJECT_PREFIX = env.str('DJANGO_EMAIL_SUBJECT_PREFIX')

EMAIL_SSL_CERTFILE = env('DJANGO_EMAIL_SSL_CERTFILE')

EMAIL_SSL_KEYFILE = env('DJANGO_EMAIL_SSL_KEYFILE')

##############################################################################
# Templates
# https://docs.djangoproject.com/en/2.0/ref/settings/#id12
##############################################################################

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [APPS_DIR.path('templates').root],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

##############################################################################
# File uploads
# https://docs.djangoproject.com/en/2.0/ref/settings/#file-uploads
##############################################################################

DEFAULT_FILE_STORAGE = env.str('DJANGO_DEFAULT_FILE_STORAGE')

FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

# https://docs.djangoproject.com/en/2.0/ref/settings/#file-upload-max-memory-size
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5 MB

FILE_UPLOAD_PERMISSIONS = None

FILE_UPLOAD_TEMP_DIR = None

MEDIA_ROOT = env.str('DJANGO_MEDIA_ROOT')
MEDIA_URL = '/media/'

STATIC_ROOT = env.str('DJANGO_STATIC_ROOT')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    APPS_DIR.path('static').root,
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

##############################################################################
# Globalization (i18n/l10n)
# https://docs.djangoproject.com/en/2.0/ref/settings/#globalization-i18n-l10n
##############################################################################

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = 'N j, Y'

DATETIME_FORMAT = 'N j, Y, P'

MONTH_DAY_FORMAT = 'F j'

SHORT_DATE_FORMAT = 'm/d/Y'

SHORT_DATETIME_FORMAT = 'm/d/Y P'

TIME_FORMAT = 'P'

YEAR_MONTH_FORMAT = 'F Y'

DATE_INPUT_FORMATS = [
    '%Y-%m-%d',  # '2006-10-25'
    '%m/%d/%Y',  # '10/25/2006'
    '%m/%d/%y',  # '10/25/06'
    '%b %d %Y',  # 'Oct 25 2006'
    '%b %d, %Y',  # 'Oct 25, 2006'
    '%d %b %Y',  # '25 Oct 2006'
    '%d %b, %Y',  # '25 Oct, 2006'
    '%B %d %Y',  # 'October 25 2006'
    '%B %d, %Y',  # 'October 25, 2006'
    '%d %B %Y',  # '25 October 2006'
    '%d %B, %Y',  # '25 October, 2006'
]

DATETIME_INPUT_FORMATS = [
    '%Y-%m-%d %H:%M:%S',  # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',  # '2006-10-25 14:30'
    '%Y-%m-%d',  # '2006-10-25'
    '%m/%d/%Y %H:%M:%S',  # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
    '%m/%d/%Y %H:%M',  # '10/25/2006 14:30'
    '%m/%d/%Y',  # '10/25/2006'
    '%m/%d/%y %H:%M:%S',  # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
    '%m/%d/%y %H:%M',  # '10/25/06 14:30'
    '%m/%d/%y',  # '10/25/06'
]

# The value must be an integer from 0 to 6, where 0 means Sunday, 1 means Monday and so on.
FIRST_DAY_OF_WEEK = 0

LANGUAGE_CODE = 'en-us'

LANGUAGES = Choices(*[(lang[0], lang[0].replace('-', '_'), lang[1]) for lang in BASE_LANGUAGES])

LOCALE_PATHS = []

##############################################################################
# Messages
# https://docs.djangoproject.com/en/2.0/ref/settings/#messages
##############################################################################

MESSAGE_LEVEL = messages.INFO

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}
{% if cookiecutter.use_cors == 'y' %}
##############################################################################
# CORS
# https://github.com/ottoyiu/django-cors-headers#configuration
##############################################################################

CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST')
{% endif %}
{%- if cookiecutter.use_allauth == 'y' %}
##############################################################################
# All Auth
# https://django-allauth.readthedocs.io/en/latest/configuration.html
##############################################################################

ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'

SOCIALACCOUNT_ADAPTER = 'allauth.socialaccount.adapter.DefaultSocialAccountAdapter'

ACCOUNT_USERNAME_BLACKLIST = env.list('ALLAUTH_USERNAME_BLACKLIST')

ACCOUNT_USER_DISPLAY = 'user.full_name'

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_AUTHENTICATION_METHOD = 'email'

ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_USER_MODEL_USERNAME_FIELD = None

ACCOUNT_EMAIL_CONFIRMATION_HMAC = True

ACCOUNT_EMAIL_SUBJECT_PREFIX = EMAIL_SUBJECT_PREFIX

ACCOUNT_DEFAULT_HTTP_PROTOCOL = DEFAULT_HTTP_PROTOCOL

ACCOUNT_FORMS = {

}

SOCIALACCOUNT_FORMS = {

}

SOCIALACCOUNT_PROVIDERS = {

}

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = env.int('ALLAUTH_CONFIRMATION_EXPIRE_DAYS')

ACCOUNT_LOGIN_ATTEMPTS_LIMIT = env.int('ALLAUTH_LOGIN_ATTEMPTS_LIMIT')

ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = env.int('ALLAUTH_LOGIN_ATTEMPTS_TIMEOUT')
{% endif %}
{%- if cookiecutter.use_rest == 'y' and cookiecutter.use_allauth == 'y' %}
##############################################################################
# Rest Auth
# https://django-rest-auth.readthedocs.io/en/latest/configuration.html
##############################################################################

REST_AUTH_SERIALIZERS = {
    # rest_auth.views.LoginView
    'LOGIN_SERIALIZER': 'rest_auth.serializers.LoginSerializer',
    # rest_auth.views.LoginView
    'TOKEN_SERIALIZER': 'rest_auth.serializers.TokenSerializer',
    # rest_auth.views.LoginView
    'JWT_SERIALIZER': 'rest_auth.serializers.JWTSerializer',
    # rest_auth.views.UserDetailsView
    'USER_DETAILS_SERIALIZER': 'rest_auth.serializers.UserDetailsSerializer',
    # rest_auth.views.PasswordResetView
    'PASSWORD_RESET_SERIALIZER': 'rest_auth.serializers.PasswordResetSerializer',
    # rest_auth.serializers.PasswordResetConfirmSerializer
    'PASSWORD_RESET_CONFIRM_SERIALIZER': 'rest_auth.serializers.PasswordResetConfirmSerializer',
    # rest_auth.views.PasswordChangeView
    'PASSWORD_CHANGE_SERIALIZER': 'rest_auth.serializers.PasswordChangeSerializer',
}

REST_AUTH_REGISTER_SERIALIZERS = {
    # rest_auth.registration.views.RegisterView
    'REGISTER_SERIALIZER': 'rest_auth.registration.serializers.RegisterSerializer'
}

REST_AUTH_TOKEN_MODEL = 'rest_framework.authtoken.models'

REST_AUTH_TOKEN_CREATOR = 'rest_auth.utils.jwt_encode'

REST_SESSION_LOGIN = True

REST_USE_JWT = True

OLD_PASSWORD_FIELD_ENABLED = True

LOGOUT_ON_PASSWORD_CHANGE = False
{% endif %}
{%- if cookiecutter.use_rest == 'y' %}
##############################################################################
# Django REST framework
# http://www.django-rest-framework.org/api-guide/settings/
##############################################################################

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': 20,
    'EXCEPTION_HANDLER': 'common.exceptions.exception_handler',
}
if not DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
    )

##############################################################################
# Django REST framework JWT
# https://getblimp.github.io/django-rest-framework-jwt/#additional-settings
##############################################################################

JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
        'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
        'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
        'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'project.apps.users.jwt.jwt_response_payload_handler',

    'JWT_SECRET_KEY': env.str('JWT_SECRET_KEY'),
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA':
        datetime.timedelta(seconds=env.int('JWT_EXPIRATION_DELTA')),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA':
        datetime.timedelta(seconds=env.int('JWT_REFRESH_EXPIRATION_DELTA')),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_AUTH_COOKIE': True,
}
{% endif %}
##############################################################################
# Django Debug Toolbar
# https://django-debug-toolbar.readthedocs.io/en/stable/configuration.html
##############################################################################

USE_DEBUG_TOOLBAR = env.bool('DJANGO_USE_DEBUG_TOOLBAR')
if USE_DEBUG_TOOLBAR:
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    # 'debug_toolbar.panels.versions.VersionsPanel'
    # 'debug_toolbar.panels.timer.TimerPanel'
    # 'debug_toolbar.panels.settings.SettingsPanel'
    # 'debug_toolbar.panels.headers.HeadersPanel'
    # 'debug_toolbar.panels.request.RequestPanel'
    # 'debug_toolbar.panels.sql.SQLPanel'
    # 'debug_toolbar.panels.staticfiles.StaticFilesPanel'
    # 'debug_toolbar.panels.templates.TemplatesPanel'
    # 'debug_toolbar.panels.cache.CachePanel'
    # 'debug_toolbar.panels.signals.SignalsPanel'
    # 'debug_toolbar.panels.logging.LoggingPanel'
    # 'debug_toolbar.panels.redirects.RedirectsPanel'
    DEBUG_TOOLBAR_CONFIG = {
        'DISABLE_PANELS': [
            'debug_toolbar.panels.redirects.RedirectsPanel',
        ],
        'RESULTS_CACHE_SIZE': 50,
        'SHOW_COLLAPSED': True,
        'PROFILER_MAX_DEPTH': 25,
        'SHOW_TEMPLATE_CONTEXT': True,
        'SQL_WARNING_THRESHOLD': 10,
        'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    }
    DEBUG_TOOLBAR_PATCH_SETTINGS = False

##############################################################################
# Debug SQL
#
##############################################################################

if env.bool('DJANGO_DEBUG_SQL'):
    LOGGING['loggers']['django.db.backends'] = {
        'handlers': ['console'],
        'propagate': False,
        'level': 'DEBUG',
    }

if env.bool('DJANGO_DEBUG_SQL_COLOR'):
    LOGGING['handlers']['console']['formatter'] = 'sql'
    LOGGING['formatters']['sql'] = {
        '()': 'common.sqlformatter.SqlFormatter',
        'format': '%(levelname)s [%(server_time)s]\n%(message)s\n',
    }

##############################################################################
# Django Silk
# https://github.com/jazzband/django-silk#configuration
##############################################################################

USE_SILK = env.bool('DJANGO_USE_SILK')
if USE_SILK:
    INSTALLED_APPS += (
        'silk',
    )
    MIDDLEWARE += (
        'silk.middleware.SilkyMiddleware',
    )
    SILKY_AUTHENTICATION = True  # User must login
    SILKY_AUTHORISATION = True  # User must have permissions
    SILKY_PERMISSIONS = lambda user: user.is_superuser
    SILKY_META = True

##############################################################################
# Sentry
# https://github.com/getsentry/raven-python
##############################################################################

if env('DJANGO_SENTRY_DSN'):
    INSTALLED_APPS += (
        'raven.contrib.django.raven_compat',
    )
    RAVEN_CONFIG = {
        'dsn': env('DJANGO_SENTRY_DSN'),
        'release': raven.fetch_git_sha(ROOT_DIR.root),
    }
    LOGGING['handlers'].update({
        'sentry': {
            'level': 'INFO',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {},
        }
    })
    LOGGING['loggers'].update({
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        }
    })

{% if cookiecutter.use_celery == 'y' %}
##############################################################################
# Celery
# http://docs.celeryproject.org/en/latest/userguide/configuration.html
##############################################################################

class CeleryConfig:
    timezone = TIME_ZONE
    beat_max_loop_interval = 5
    beat_sync_every = 1
    broker_url = env.str('CELERY_BROKER_URL')
    result_backend = env.str('CELERY_RESULT_BACKEND')
    task_always_eager = env.bool('CELERY_ALWAYS_EAGER')
    task_ignore_result = env.bool('CELERY_IGNORE_RESULT')
    task_default_queue = 'normal'
    task_default_exchange = 'normal'
    task_default_routing_key = 'normal'
    {%- if cookiecutter.use_rabbitmq == 'y' %}
    task_queues = (
        Queue('high', Exchange('high'), routing_key='high'),
        Queue('normal', Exchange('normal'), routing_key='normal'),
        Queue('low', Exchange('low'), routing_key='low'),
    )
    {%- endif %}
    worker_max_tasks_per_child = 1000
    worker_max_memory_per_child = 12000  # 12MB
{%- endif %}
