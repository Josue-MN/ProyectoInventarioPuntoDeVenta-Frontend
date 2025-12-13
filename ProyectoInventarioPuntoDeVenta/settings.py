"""
Django settings for ProyectoInventarioPuntoDeVenta project.
FRONTEND PURO – CONSUME API JWT
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-o53sd!o+xpkb90f*q#@in5$lllhjue9-imq3nh)s!eo3)qd*is'

DEBUG = True

ALLOWED_HOSTS = []

# -------------------------------------------------
# SESIONES SIN BASE DE DATOS
# -------------------------------------------------
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

# -------------------------------------------------
# APLICACIONES
# -------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    # Apps de frontend (templates + views)
    'LoginApp',
    'AdminHomeApp',
    'HomeApp',
    'CrudEmpleadosApp',
    'CrudProductosApp',
    'CrudCategoriaProductoApp',
    'CrudBodegasApp',
    'CrudCargosApp',
    'CrudUsuariosApp',
    'AuditoriaApp',
]

# -------------------------------------------------
# MIDDLEWARE (SIN messages / auth DB)
# -------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ProyectoInventarioPuntoDeVenta.urls'

# -------------------------------------------------
# TEMPLATES
# -------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'ProyectoInventarioPuntoDeVenta.wsgi.application'

# -------------------------------------------------
# ❌ BASE DE DATOS DESACTIVADA
# -------------------------------------------------
DATABASES = {}

# -------------------------------------------------
# INTERNACIONALIZACIÓN
# -------------------------------------------------
LANGUAGE_CODE = 'es-cl'

TIME_ZONE = 'America/Santiago'

USE_I18N = True
USE_TZ = True

DATE_INPUT_FORMATS = ['%d-%m-%Y']
DATE_FORMAT = 'd-m-Y'

# -------------------------------------------------
# STATIC FILES
# -------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
