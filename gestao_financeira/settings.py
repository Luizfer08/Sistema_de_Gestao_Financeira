from pathlib import Path

# BASE DO PROJETO
BASE_DIR = Path(__file__).resolve().parent.parent


#  SEGURANÇA
SECRET_KEY = 'django-insecure-sua-chave-aqui'

DEBUG = True

ALLOWED_HOSTS = []


#  APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # seu app
    'financeiro',
]


#  MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    # CSRF importante para login funcionar
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


#  URL PRINCIPAL
ROOT_URLCONF = 'gestao_financeira.urls'


#  TEMPLATES (CORRIGIDO)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # CAMINHO CERTO DOS HTML
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


#  BANCO (DESENVOLVIMENTO)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


#  VALIDAÇÃO DE SENHA
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


#  STATIC (CSS / JS)
STATIC_URL = '/static/'

#  CAMINHO DOS ARQUIVOS STATIC
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]


#  LOGIN / LOGOUT
LOGIN_URL = 'financeiro:login'
LOGIN_REDIRECT_URL = 'financeiro:dashboard'
LOGOUT_REDIRECT_URL = 'financeiro:login'


#  DEFAULT
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'