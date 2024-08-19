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