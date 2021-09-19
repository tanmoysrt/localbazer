import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'flcxo$4rz*(abdwun+qa-1i-ox8(#(r)1f+mxzzpltrlul^s5l'

DEBUG =True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'mathfilters',
    'sorl.thumbnail',
    'accounts.apps.AccountsConfig',
    'buyer.apps.BuyerConfig',
    'seller.apps.SellerConfig',
    'datamanagement.apps.DatamanagementConfig',
    'checkout.apps.CheckoutConfig',
    'shopqrhandler.apps.ShopqrhandlerConfig',
    'referral1.apps.Referral1Config',
    'api.apps.ApiConfig',
    'adminpanel.apps.AdminpanelConfig',
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

ROOT_URLCONF = 'localbazeer.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'localbazeer.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'localbazerdb',
        'USER': 'tanmoypratim',
        'PASSWORD': 'pgtn001@*^#',
        'HOST': 'localhost',
        'PORT': '',
    }
}




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


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_URL='buyerlogin'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')
MEDIA_URL='/media/'


# Fast2sms API Configuration

headers = {
    'authorization': "osWut3ZgKeVPQQ7IQVjXBbCmQU5TGJ424Lkz17SV2SZ2VzmiTezRnbdoQbCG",
    'cache-control': "no-cache",
    'content-type': "application/x-www-form-urlencoded"
    }
url = "https://www.fast2sms.com/dev/bulk"
