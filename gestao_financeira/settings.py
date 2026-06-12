from pathlib import Path
import os

from dotenv import load_dotenv


# BASE

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()


# Converte variaveis de ambiente textuais em booleanos.
def env_bool(nome, padrao=False):

    valor = os.environ.get(nome)

    if valor is None:

        return padrao

    return valor.strip().lower() in {
        '1',
        'true',
        'yes',
        'on',
        'sim'
    }


# Converte listas separadas por virgula vindas do arquivo .env.
def env_list(nome, padrao=None):

    valor = os.environ.get(nome)

    if not valor:

        return padrao or []

    return [
        item.strip()
        for item in valor.split(',')
        if item.strip()
    ]


# Em producao, a chave secreta precisa existir e ser fixa.
SECRET_KEY = os.environ.get('SECRET_KEY')

if not SECRET_KEY:

    raise RuntimeError(
        'Configure a variavel SECRET_KEY no arquivo .env.'
    )


# DEBUG deve ser ligado apenas em desenvolvimento.
DEBUG = env_bool('DEBUG', False)


# Em producao, informe os dominios permitidos no .env.
ALLOWED_HOSTS = env_list(
    'ALLOWED_HOSTS',
    ['127.0.0.1', 'localhost'] if DEBUG else []
)

if not DEBUG and not ALLOWED_HOSTS:

    raise RuntimeError(
        'Configure ALLOWED_HOSTS no arquivo .env para producao.'
    )


# APPS

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # App principal do projeto.
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


# URL PRINCIPAL

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


# WSGI

WSGI_APPLICATION = 'gestao_financeira.wsgi.application'


# DATABASE

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
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]


# LOCALIZACAO

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True
USE_TZ = True


# STATIC FILES

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'


# AUTH REDIRECT

LOGIN_URL = 'financeiro:login'
LOGIN_REDIRECT_URL = 'financeiro:dashboard'
LOGOUT_REDIRECT_URL = 'financeiro:login'


# SEGURANCA

X_FRAME_OPTIONS = 'DENY'

# Cookies seguros ficam ativos por padrao quando DEBUG esta desligado.
SESSION_COOKIE_SECURE = env_bool(
    'SESSION_COOKIE_SECURE',
    not DEBUG
)
CSRF_COOKIE_SECURE = env_bool(
    'CSRF_COOKIE_SECURE',
    not DEBUG
)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'same-origin'

# Use somente em producao com HTTPS configurado.
SECURE_SSL_REDIRECT = env_bool(
    'SECURE_SSL_REDIRECT',
    False
)

CSRF_TRUSTED_ORIGINS = env_list(
    'CSRF_TRUSTED_ORIGINS'
)


# EMAIL USUARIO

EMAIL_HOST_USER = os.environ.get('EMAIL_USER')

# EMAIL SENHA

EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')


# CONFIGURACAO SMTP

if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:

    # Backend real para envio por SMTP.
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    # Servidor Gmail.
    EMAIL_HOST = 'smtp.gmail.com'

    # Porta TLS.
    EMAIL_PORT = 587

    # Seguranca TLS.
    EMAIL_USE_TLS = True

    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    SERVER_EMAIL = EMAIL_HOST_USER

else:

    # Em desenvolvimento sem SMTP, o e-mail aparece no terminal.
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
