from django.core.cache import caches, cache, ConnectionProxy
from django_redis.cache import RedisCache

# from mubai_service import settings


default_cache: RedisCache = caches
encryption_key_cache: RedisCache = ConnectionProxy(caches, "encryption")

