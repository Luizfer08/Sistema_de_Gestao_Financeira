from pathlib import Path
import os
from dotenv import load_dotenv
from django.core.management.utils import get_random_secret_key

# BASE

BASE_DIR = Path(__file__).resolve().parent.parent

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')

if not SECRET_KEY:
    print(" SECRET_KEY não encontrada, gerando chave temporária...")
    SECRET_KEY = get_random_secret_key()

DEBUG = True

ALLOWED_HOSTS = []


# APPS

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # apps do projeto
    'usuarios',
    'financeiro',
]


# MIDDLEWARE

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


#  URL PRINCIPAL
ROOT_URLCONF = 'gestao_financeira.urls'


# TEMPLATES

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        
        'DIRS': [BASE_DIR / 'templates'],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


#  WSGI
WSGI_APPLICATION = 'gestao_financeira.wsgi.application'

# DATABASE

load_dotenv() 
DATABASES = { 
    'default': { 
        'ENGINE': 'django.db.backends.postgresql', 
        'NAME': os.getenv('DB_NAME'), 
        'USER': os.getenv('DB_USER'), 
        'PASSWORD': os.getenv('DB_PASSWORD'), 
        'HOST': os.getenv('DB_HOST'), 
        'PORT': os.getenv('DB_PORT'), 
    } 
}


# PASSWORD

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



LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True
USE_TZ = True


# STATIC FILES
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

STATIC_ROOT = BASE_DIR / 'staticfiles'


# AUTH REDIRECT

LOGIN_URL = 'financeiro:login'
LOGIN_REDIRECT_URL = 'financeiro:dashboard'
LOGOUT_REDIRECT_URL = 'financeiro:login'

# SEGURANÇA 
X_FRAME_OPTIONS = 'DENY'

# DESATIVA EM DESENVOLVIMENTO (senão quebra login)
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False


# EMAIL (OPCIONAL)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
