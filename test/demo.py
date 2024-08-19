


import os
import django

# 设置 DJANGO_SETTINGS_MODULE 环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

# 初始化 Django
django.setup()

# 现在你可以使用 django-redis 了
from django.core.cache import cache,caches,ConnectionProxy
from django_redis import get_redis_connection
from django_redis.cache import RedisCache
# 示例操作
# cache.set('my_key', 'my_value',20)
cache:RedisCache
value = cache.get('my_key')
print(value)  # 输出: my_value
# print(cache._alias)
# print(dir(cache))
# print(dir(cache._connections))
# print(dir(cache._connections['default']))
# print(type(cache._connections['default']))
# redis_conn = get_redis_connection("default")

print(cache.pttl("my_key"))
print(cache.pttl("my_key"))
print(cache.pttl("my_key"))
print(cache.ttl("my_key"))
print(cache.ttl("my_key"))
print(cache.ttl("my_key"))
print(cache.pttl("my_key"))


# 查看缓存的剩余过期时间（以秒为单位）
# ttl = redis_conn.ttl("my_key")
# print(f"Remaining TTL for 'my_key': {ttl} seconds")
#
# # 获取并打印缓存的值
# value = cache.get('my_key')
# print(f"Value of 'my_key': {value}")

last = ConnectionProxy(caches,"encryption")

print(last)

# last.set('my_key1', 'my_value',24*60*60)
# last.set('my_key1', 'my_value',24*60*60)


value = last.get('my_key1')
print(value)  # 输出: my_value
print(value is None)
value = last.get('my_key')
print(value)  # 输出: my_value