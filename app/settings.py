"""
Django settings for app project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in ('1', 'true', 'yes', 'on')


def env_list(name, default=''):
    value = os.environ.get(name, default)
    return [item.strip() for item in value.split(',') if item.strip()]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
MIN_SECRET_KEY_LENGTH = 32
DEBUG = env_bool('DJANGO_DEBUG', False)

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if SECRET_KEY:
    SECRET_KEY = SECRET_KEY.strip()
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = 'unsafe-development-secret-key'
    else:
        raise RuntimeError(
            'DJANGO_SECRET_KEY must be set unless DJANGO_DEBUG is enabled for local development.'
        )
if not DEBUG and len(SECRET_KEY) < MIN_SECRET_KEY_LENGTH:
    raise RuntimeError(
        'DJANGO_SECRET_KEY must be at least 32 characters when DJANGO_DEBUG is disabled.'
    )

# SECURITY WARNING: don't run with debug turned on in production!
TEMPLATE_DEBUG = DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

ALLOWED_HOSTS = env_list(
    'DJANGO_ALLOWED_HOSTS',
    'localhost,127.0.0.1' if DEBUG else ''
)
if not DEBUG and not ALLOWED_HOSTS:
    raise RuntimeError(
        'DJANGO_ALLOWED_HOSTS must be set unless DJANGO_DEBUG is enabled for local development.'
    )
if not DEBUG and '*' in ALLOWED_HOSTS:
    raise RuntimeError(
        'DJANGO_ALLOWED_HOSTS must not contain wildcard hosts when DJANGO_DEBUG is disabled.'
    )


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'south',
    'app',
    'home'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
)

ROOT_URLCONF = 'app.urls'

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ.get('DJANGO_SQLITE_PATH', os.path.join(BASE_DIR, 'db.sqlite3')),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# Get your Twitter key/secret from the Twitter developer portal.
SOCIAL_AUTH_TWITTER_KEY = os.environ.get('SOCIAL_AUTH_TWITTER_KEY', '')
SOCIAL_AUTH_TWITTER_SECRET = os.environ.get('SOCIAL_AUTH_TWITTER_SECRET', '')

TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN', '')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET', '')

SOCIAL_AUTH_BEATS_KEY = os.environ.get('SOCIAL_AUTH_BEATS_KEY', '')
SOCIAL_AUTH_BEATS_SECRET = os.environ.get('SOCIAL_AUTH_BEATS_SECRET', '')

SOCIAL_AUTH_SPOTIFY_KEY = os.environ.get('SOCIAL_AUTH_SPOTIFY_KEY', '')
SOCIAL_AUTH_SPOTIFY_SECRET = os.environ.get('SOCIAL_AUTH_SPOTIFY_SECRET', '')

SOCIAL_AUTH_LOGIN_URL          = '/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_ERROR_URL    = '/login-error/'

SOCIAL_AUTH_REVOKE_TOKENS_ON_DISCONNECT = True

LOGIN_URL = '/login/twitter'
