"""
Django settings for wwf_prince project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from django.utils.encoding import smart_str
import django
django.utils.encoding.smart_text = smart_str
from sentry_sdk.integrations.django import DjangoIntegration
import sentry_sdk
from django.contrib import messages
import environ
from django.urls import reverse_lazy
from pathlib import Path
from decouple import config
import os


#ugettext_lazy has been removed in Django 4.0 366. Please use gettext_lazy instead:
# from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: BASE_DIR / "directory"
BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATICFILES_DIRS = [str(BASE_DIR / 'static'), ]
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn")
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_cdn")

# Use Django templates using the new Django 1.8 TEMPLATES settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(BASE_DIR / 'templates'),
            # insert more TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.context_processors.auth',
            ],
        },
    },
]

# Use 12factor inspired environment variables or from a file
env = environ.Env()

# Create a local.env file in the settings directory
# But ideally this env file should be outside the git repo
env_file = Path(__file__).resolve().parent / 'local.env'
if env_file.exists():
    environ.Env.read_env(str(env_file))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# Application definition

SITE_ID = 1
SITE = 1
INSTALLED_APPS = (
    'admin_interface',
    'colorfield',
    'dal', # https://django-autocomplete-light.readthedocs.io/en/master/install.html
    'dal_select2',
    'localflavor',
    'tinymce',
    'filebrowser',    
    
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.postgres',

    'authtools', # https://django-authtools.readthedocs.io/en/latest/
    'crispy_forms',
    #'easy_thumbnails',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework_datatables',
    'django_extensions',
    'related_admin',  # handles related field display in admins

    'ajax_select',
    'ordered_model', # https://github.com/bfirsh/django-ordered-model
    'imagekit',
    'sorl.thumbnail',
    'leaflet',
    'djgeojson',
    'django_filters',
    'cookielaw',
    'phonenumber_field',
    'django_tables2',
    'controlcenter', # https://django-controlcenter.readthedocs.io/en/latest/examples.html
    'profiles',
    'accounts',
    'observations',
    'news',
    'utils',

    'debug_permissions',
    'dbbackup_ui',
    'captcha', # https://pypi.org/project/django-recaptcha/#requirements
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crum.CurrentRequestUserMiddleware',
    'admin_log.middleware.AdminLogMiddleware'    
]

ROOT_URLCONF = 'wwf_prince.urls'

WSGI_APPLICATION = 'wwf_prince.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PW'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
    },
}

DEFAULT_FROM_EMAIL = 'Save the Prince Admin <salvataggioanfibi@gmail.com>'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SERVER_EMAIL = config("EMAIL_HOST_USER")
EMAIL_HOST_USER = config("EMAIL_HOST_USER"),
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD"),



# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'it-IT'

TIME_ZONE = 'Europe/Rome'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

ALLOWED_HOSTS = ["*"]

# Crispy Form Theme - Bootstrap 3
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# For Bootstrap 3, change error alert to 'danger'
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# Authentication Settings
AUTH_USER_MODEL = 'authtools.User'
LOGIN_REDIRECT_URL = reverse_lazy("profiles:show_self")
LOGIN_URL = reverse_lazy("accounts:login")

THUMBNAIL_EXTENSION = 'jpg'     # Or any extn for your thumbnails
TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 1120,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': '''
            link image preview
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}

FILEBROWSER_DIRECTORY = ''
DIRECTORY = ''
FILEBROWSER_MAX_UPLOAD_SIZE = 50000000

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_datatables.renderers.DatatablesRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_datatables.filters.DatatablesFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_datatables.pagination.DatatablesPageNumberPagination',
    'PAGE_SIZE': 25,
}
def before_send(event, hint):
    """Don't log django.DisallowedHost errors in Sentry."""
    if 'log_record' in hint:
        if hint['log_record'].name == 'django.security.DisallowedHost':
            return None
    return event
sentry_sdk.init(
    dsn="https://cbe9d6ead2b94423813e5efbccad9458@sentry.io/1909095",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    before_send=before_send
)


LEAFLET_CONFIG = {
    # 'TILES': [],
    'DEFAULT_CENTER': (45.5004614,10.1203557),
    'DEFAULT_ZOOM': 10,
    'SPATIAL_EXTENT': (4.0, 42.0, 20, 50)
}


# CAPTCHA
RECAPTCHA_PUBLIC_KEY = config('CAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = config('CAPTCHA_PRIVATE_KEY')
