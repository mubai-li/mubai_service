from mubai_service.default_settings import *

# 自己添加的内容
import os

if not DEBUG:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mubai_service',
        'USER': 'root',
        'PASSWORD': '1208',
        'HOST': 'localhost',  # 或者你的数据库服务器地址
        'PORT': '3306',  # 默认端口是3306
    }

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# AUTH_USER_MODEL = 'api.user'  # 在使用django自带的auth用户表的时候一定需要配置这个参数

# restframework 配置
INSTALLED_APPS.append("rest_framework")

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [  # 默认响应渲染类
        'rest_framework.renderers.JSONRenderer',  # json渲染器
        'rest_framework.renderers.BrowsableAPIRenderer',  # 自带的浏览API渲染器，如果是TemplateHTMLRenderer可以设置自定义的模板返回数据
    ],
    'DEFAULT_PARSER_CLASSES': [  # 默认分析器类
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_FILTER_BACKENDS': []
}
# django_filter 配置
INSTALLED_APPS.append('django_filters')

REST_FRAMEWORK['DEFAULT_FILTER_BACKENDS'].append('django_filters.rest_framework.DjangoFilterBackend')
