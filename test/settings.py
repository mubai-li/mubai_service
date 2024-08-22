# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://172.23.80.150:6379/1",  # Redis 服务器的地址和数据库编号
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     },
#     "encryption": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://172.23.80.150:6379/0",  # Redis 服务器的地址和数据库编号
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }


import django
from django.conf import settings
from redis.client import Redis
# 配置Django设置模块
settings.configure(
    CACHES={
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://172.23.80.150:6379/1",  # Redis 服务器的地址和数据库编号
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },

    }
)

# 初始化Django
django.setup()


# 获取Redis连接
from django.core.cache import caches, cache, ConnectionProxy
from django_redis.cache import RedisCache
from django_redis import get_redis_connection
print(type(cache))

cache:RedisCache

cache.set("data",1)
print(cache.get("data"))

r:Redis = cache.client.get_client(write=True)
# r = get_redis_connection("default")


print(r.get("data"))
print(cache.get("data"))

