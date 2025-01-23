from django.core.cache import caches, cache, ConnectionProxy
from django_redis.cache import RedisCache

# from mubai_service import settings


default_cache: RedisCache = caches
# 加密池缓存
encryption_key_cache: RedisCache = ConnectionProxy(caches, "encryption")
# 验证码缓存池
verification_key_cache: RedisCache = ConnectionProxy(caches, "verification")

