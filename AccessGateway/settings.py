"""
Django settings for AccessGateway project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2(992yeffkdir4-g43n6a02raw)vshhwq1l+x_%v(wa0n0px6^'


# SECURITY WARNING: don't run with debug turned on in production!
# 如果设置成了False ,讲无法调用Setting中的路径设置
# 调试开发环境下需要True , 运营上线环境下，需要False
DEBUG = True     # 默认是True  请不要在生产环境中使用Debug，会造成内容溢出

# ALLOWED_HOSTS = []  # 容许本地访问
ALLOWED_HOSTS = ["*"]  # 容许所有人访问

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_celery_beat',
    # 'djcelery',
    'Web.apps.WebConfig',

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

ROOT_URLCONF = 'AccessGateway.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'AccessGateway.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
#sqlite3
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# mysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'accessgateway',
        'USER': 'accessgateway',
        'PASSWORD': '7ECgIfMhjNhsIzzX',
        'HOST': '0.0.0.0',
        'PORT': '3306',
        'OPTIONS':{"init_command": "SET foreign_key_checks = 0;",}
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Toronto'
# 关闭 UTC
USE_TZ = True
CELERY_ENABLE_UTC = False
# 设置 django-celery-beat 真正使用的时区
CELERY_TIMEZONE = TIME_ZONE
# 使用 timezone naive 模式
DJANGO_CELERY_BEAT_TZ_AWARE = False

USE_I18N = True

USE_L10N = True


APPEND_SLASH = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "statics"),
]
# 修改自定义用户
AUTH_USER_MODEL = 'Web.UserProfile'

# 验证登录装饰器
LOGIN_URL = '/login/'

# 文件下载路径
DOWNLOAD_PATH = "%s/downloads/" % BASE_DIR

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# for celery
CELERY_BROKER_URL = 'redis://localhost'
CELERY_RESULT_BACKEND = 'redis://localhost'

# CELERY_BROKER_URL = 'redis://:kf48#$2Y0!!Mdg9QNMh^4T&S$wdb$6v*51@35.183.17.205:6379'
# CELERY_RESULT_BACKEND = 'redis://:kf48#$2Y0!!Mdg9QNMh^4T&S$wdb$6v*51@35.183.17.205:6379'

#############################
# celery 配置信息 start
#############################
# import djcelery
# djcelery.setup_loader() # 遍历搜索所有APP下的tasks.py任务
# BROKER_URL = 'redis://127.0.0.1:6379/1'
# CELERY_IMPORTS = ('Web.tasks')
# CELERY_TIMEZONE = 'America/Toronto'
# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'  # 默认使用系统django项目配置的数据库
# # CELERY_ENABLE_UTC = True  # 是否在同一时区，false是不同时区
# # CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'yaml']  # 允许的格式
# # BROKER_TRANSPORT = 'redis'  # redis作为中间件
# # 下面是定时任务的设置，我一共配置了三个定时任务.
# from celery.schedules import crontab
# CELERYBEAT_SCHEDULE = {
#     #定时任务一：　每24小时周期执行任务(del_redis_data)
#     u'删除过期的redis数据': {
#         "task": "app.tasks.del_redis_data",
#         "schedule": crontab(hour='*/24'),
#         "args": (),
#     },
#     #定时任务二:　每天的凌晨12:30分，执行任务(back_up1)
#     u'生成日报表': {
#         'task': 'app.tasks.back_up1',
#         'schedule': crontab(minute=30, hour=0),
#         "args": ()
#     },
#     #定时任务三:每个月的１号的6:00启动，执行任务(back_up2)
#     u'生成统计报表': {
#             'task': 'app.tasks.back_up2',
#             'schedule': crontab(hour=6, minute=0,   day_of_month='1'),
#             "args": ()
#     },
# }
#############################
# celery 配置信息 end
#############################
# 配置参数
# # Celery
# import djcelery
# djcelery.setup_loader()  # 当 djcelery.setup_loader() 运行时，Celery 便会去查看 INSTALLD_APPS 下包含的所有 app 目录中的 tasks.py 文件，找到标记为task 的方法，将它们注册为 celery task.
# CELERY_TIMEZONE = 'America/Toronto'
# CELERY_ENABLE_UTC = True  #是否在同一时区，false是不同时区
# CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'yaml']  # 允许的格式
# BROKER_URL = 'redis://127.0.0.1:6379/0'  # redis作为中间件 负责分发任务给 worker 去执行
# BROKER_TRANSPORT = 'redis'
# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'  # 默认使用系统设置好的什么数据库，
# # CELERY_DEFAULT_QUEUE：默认队列
# # BROKER_URL  : 代理人即rabbitmq的网址
# # CELERY_RESULT_BACKEND：结果存储地址
# # CELERY_TASK_SERIALIZER：任务序列化方式
# # CELERY_RESULT_SERIALIZER：任务执行结果序列化方式
# # CELERY_TASK_RESULT_EXPIRES：任务过期时间
# # CELERY_ACCEPT_CONTENT：指定任务接受的内容序列化类型(序列化)，一个列表；
# # CELERYD_LOG_FILE = BASE_DIR + "/logs/celery/celery.log"         # log路径
# # CELERYBEAT_LOG_FILE = BASE_DIR + "/logs/celery/beat.log"     # beat log路径
# ##########################
