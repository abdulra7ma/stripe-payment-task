# external imports
from redis.exceptions import RedisError


class CacheKeyNotFound(RedisError):
    pass
