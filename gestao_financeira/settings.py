

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-evgrcqoh8tp$9g^xvu^5*unm=3f-q%5kof(g@md&0ff2a2j2td'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin', # painel administrativo padrão do Django
    'django.contrib.auth',  # sistema de autenticação de usuários
    'django.contrib.contenttypes',  # gerenciamento interno de tipos de conteúdo
    'django.contrib.sessions', # controle de sessões de usuários logados
    'django.contrib.messages', # sistema de mensagens do Django
    'django.contrib.staticfiles', # gerenciamento de arquivos estáticos (CSS, JS, imagens)
    'usuarios', # app responsável por cadastro e autenticação de usuários
    'financeiro', # app responsável pelo controle financeiro do sistema
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gestao_financeira.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
<<<<<<< HEAD
        'DIRS': [BASE_DIR /'templates'], # diretório onde ficam os arquivos de template HTML
=======
        'DIRS': ['templates'], # diretório onde ficam os arquivos de template HTML
>>>>>>> 41671f439d7288a09add963222182e842cab175e
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

WSGI_APPLICATION = 'gestao_financeira.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

<<<<<<< HEAD
LOGIN_URL = 'financeiro:home'
LOGIN_REDIRECT_URL = 'financeiro:dashboard'
LOGOUT_REDIRECT_URL = 'financeiro:home'
=======
LOGIN_URL = '/login/'
# se não estiver logado, manda pro login

LOGIN_REDIRECT_URL = '/'
# depois do login, vai pro dashboard
>>>>>>> 41671f439d7288a09add963222182e842cab175e

# impede cliquejacking
X_FRAME_OPTIONS = 'DENY'

# força cookies seguros
SESSION_COOKIE_SECURE = True

# protege CSRF via HTTPS
CSRF_COOKIE_SECURE = True

# CONFIGURAÇÃO EMAIL (GMAIL)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'seuemail@gmail.com'

EMAIL_HOST_PASSWORD = 'senha_app_gmail'

<<<<<<< HEAD
=======
LOGIN_REDIRECT_URL = '/dashboard/'
>>>>>>> 41671f439d7288a09add963222182e842cab175e
