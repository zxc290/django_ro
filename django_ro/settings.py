"""
Django settings for django_ro project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zs_yvs^$n38hyba0sctx6fk1f6j00=qz7*v+-3#gj^5k*$nvtx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'ro_operations',
    'corsheaders',
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

ROOT_URLCONF = 'django_ro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'django_ro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     # 数据库引擎设置
    #     'ENGINE': 'sql_server.pyodbc',
    #     # 要连接的数据库名
    #     'NAME': 'ServerAdmin',
    #     # 数据库用户名
    #     'USER': 'DB_rwAccount!QAZ',
    #     # 数据库密码
    #     'PASSWORD': 'DB_dhJ15*edqdI',
    #     # 数据库主机地址
    #     'HOST': 'auth.xgd666.com,10097',
    #     # 数据库端口号，默认可以不写
    #     'PORT': '',
    #     # 选项，这个要先在操作系统上完成ODBC的连接创建，并连接成功，注意10.0这个地方，要和自己的ODBC版本一致
    #     'OPTIONS': {
    #         'driver': 'SQL Server Native Client 10.0',
    #     },
    # },
    'default': {
        # 数据库引擎设置
        'ENGINE': 'sql_server.pyodbc',
        # 要连接的数据库名
        'NAME': 'ServerAdminRo',
        # 数据库用户名
        'USER': 'sa',
        # 数据库密码
        'PASSWORD': '7cool_7COOL_7cool',
        # 数据库主机地址
        'HOST': '127.0.0.1',
        # 数据库端口号，默认可以不写
        'PORT': '',
        # 选项，这个要先在操作系统上完成ODBC的连接创建，并连接成功，注意10.0这个地方，要和自己的ODBC版本一致
        'OPTIONS': {
            'driver': 'SQL Server Native Client 10.0',
        },
    },
    'server_management': {
        # 数据库引擎设置
        'ENGINE': 'sql_server.pyodbc',
        # 要连接的数据库名
        'NAME': 'ServerManagementRo',
        # 数据库用户名
        'USER': 'sa',
        # 数据库密码
        'PASSWORD': '7cool_7COOL_7cool',
        # 数据库主机地址
        'HOST': '127.0.0.1',
        # 数据库端口号，默认可以不写
        'PORT': '',
        # 选项，这个要先在操作系统上完成ODBC的连接创建，并连接成功，注意10.0这个地方，要和自己的ODBC版本一致
        'OPTIONS': {
            'driver': 'SQL Server Native Client 10.0',
        },
    },
    'appid_management': {
         # 数据库引擎设置
        'ENGINE': 'sql_server.pyodbc',
        # 要连接的数据库名
        'NAME': 'AppidManagementRo',
        # 数据库用户名
        'USER': 'sa',
        # 数据库密码
        'PASSWORD': '7cool_7COOL_7cool',
        # 数据库主机地址
        'HOST': '127.0.0.1',
        # 数据库端口号，默认可以不写
        'PORT': '',
        # 选项，这个要先在操作系统上完成ODBC的连接创建，并连接成功，注意10.0这个地方，要和自己的ODBC版本一致
        'OPTIONS': {
            'driver': 'SQL Server Native Client 10.0',
        },
    }
}

# DATABASE_ROUTERS = ['django_ro.database_router.DatabaseAppsRouter']
# DATABASE_APPS_MAPPING = {
#     # example:
#     #'app_name':'database_name',
#     # 'server_admin': 'server_admin',
#     'appid_management': 'appid_management',
# }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'


# 跨域设置
CORS_ORIGIN_ALLOW_ALL = True


FID_PERMISSION = '(196)'