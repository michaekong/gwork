# myproject/settings.py

import os
from pathlib import Path
# import dj_database_url # Plus nécessaire pour SQLite

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Votre clé secrète fournie
SECRET_KEY = 'django-insecure-x_rd@@&n458dn1a^#@cqcm+w*ytgse70$im#0mwrvoyf0*cvq='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True # À changer en False pour la production !

ALLOWED_HOSTS = [] # Ajoutez les noms de domaine de votre production ici, ex: ['.render.com', 'votre-domaine.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ninja', # Ajout de Django Ninja
    'authentification', # Votre application d'authentification
    # Ajoutez ici d'autres applications Django si vous en avez
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

ROOT_URLCONF = 'gwork.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'authentification', 'Template')],
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

WSGI_APPLICATION = 'gwork.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Utilisation de la base de données SQLite par défaut de Django
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# Modèle d'utilisateur personnalisé
AUTH_USER_MODEL = 'authentification.Utilisateur'


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'fr-fr' # Langue française

TIME_ZONE = 'Africa/Douala' # Fuseau horaire pour Yaoundé, Cameroun

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
# settings.py

STATIC_URL = '/static/'

# Optionnel : Si vous avez besoin de spécifier un répertoire pour les fichiers statiques
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Assurez-vous que cela correspond à votre structure
]
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Où les fichiers statiques seront collectés en production
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- Configurations spécifiques à l'application G-work ---

# Configuration Email (pour l'envoi d'emails de vérification, etc.)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com' # Votre hôte SMTP
EMAIL_PORT = 587 # Votre port SMTP
EMAIL_USE_TLS = True # Utiliser TLS
EMAIL_HOST_USER = 'memocloudenstp@gmail.com' # Votre adresse email
EMAIL_HOST_PASSWORD = 'ixyu qgxy lksn ickb' # Votre mot de passe d'application Gmail
DEFAULT_FROM_EMAIL = 'no-reply@g-work.com' # Adresse email par défaut pour l'envoi

# Configuration JWT pour l'authentification
# Il est recommandé d'utiliser une clé différente de SECRET_KEY en production
JWT_SECRET_KEY = SECRET_KEY # Pour cet exemple, nous utilisons la même clé secrète de Django
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_HOURS = 24 # Token valide 24 heures

# Configuration de la vérification d'email
EMAIL_VERIFICATION_SALT = "VOTRE_SEL_UNIQUE_ET_SECRET_POUR_LA_VERIFICATION_EMAIL" # À changer en production !
FRONTEND_URL = 'https://gwork.onrender.com/auth/auth' # URL de votre application frontend (React, Vue, etc.)
# settings.py

# Par exemple, pour permettre jusqu’à 10 Mo :
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
