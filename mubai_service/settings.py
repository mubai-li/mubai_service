from mubai_service.default_settings import *

# 自己添加的内容
import os

DEBUG = True
JWTToken = True
# 重定向

APPEND_SLASH = True

if not DEBUG:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mubai_service',
        'USER': 'root',
        'PASSWORD': '1208',
        'HOST': 'localhost',  # 或者你的数据库服务器地址
        'PORT': '3306',  # 默认端口是3306
    }
# 添加media
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# 添加静态文件
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]  # 这个表示的是静态文件夹的路径

# 注册的app
INSTALLED_APPS.append("apps.user_app")
INSTALLED_APPS.append("apps.file_app")
# INSTALLED_APPS.append("django_filters")

# 注册User
AUTH_USER_MODEL = 'user_app.UserModel'  # 在使用django自带的auth用户表的时候一定需要配置这个参数

# INSTALLED_APPS.append("apps.user_app.apps.UserAppConfig")
# 添加支持的ip
if DEBUG:
    ALLOWED_HOSTS.append("*")
else:
    ALLOWED_HOSTS.append("0.0.0.0")
# rest framework 配置
INSTALLED_APPS.append("rest_framework.authtoken")
INSTALLED_APPS.append("rest_framework")
INSTALLED_APPS.append("rest_framework_jwt")

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [  # 默认响应渲染类
        'rest_framework.renderers.JSONRenderer',  # json渲染器
        'rest_framework.renderers.BrowsableAPIRenderer',  # 自带的浏览API渲染器，如果是TemplateHTMLRenderer可以设置自定义的模板返回数据
    ],
    'DEFAULT_PARSER_CLASSES': [  # 默认分析器类
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',  # 添加 MultiPartParser
        'rest_framework.parsers.FileUploadParser',  # 添加 FileUploadParser
    ],
    'DEFAULT_FILTER_BACKENDS': []
}
if JWTToken:
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'].append('rest_framework_jwt.authentication.JSONWebTokenAuthentication')
else:
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'].append('rest_framework_jwt.authentication.TokenAuthentication')

# django_filter 配置
INSTALLED_APPS.append('django_filters')

REST_FRAMEWORK['DEFAULT_FILTER_BACKENDS'].append('django_filters.rest_framework.DjangoFilterBackend')
# 自定义的中间件
# MIDDLEWARE.append("utils.project_middlewave.data_encryption.DataEncryptionMiddleware")
# 自定义日志系统

# django_log_path =

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{levelname} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'file_app': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': r'C:\Users\32509\Desktop\myproject\mubai_service\logs\django.log',
#             'formatter': 'verbose',
#         },
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file_app', 'console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'myapp': {
#             'handlers': ['file_app', 'console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }
# redis配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://172.23.80.150:6379/1",  # Redis 服务器的地址和数据库编号
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "encryption": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://172.23.80.150:6379/0",  # Redis 服务器的地址和数据库编号
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
# 定义 cahe的时间
caches_time = 24 * 60 * 60

import datetime

# 定义jwt的时间
JWT_AUTH = {
    # 'JWT_RESPONSE_PAYLOAD_HANDLER': 'api.utils.my_jwt_response_payload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=12.0),
    "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(days=0),  # 这个表示登录之后刷新一次将会重新生成一个新的jwt数据
}
