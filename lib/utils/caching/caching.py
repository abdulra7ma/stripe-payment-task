# Python imports
import json

# Django imports
from django.apps import apps
from django.db import models

from redis.exceptions import DataError

# external imports
import redis

# app imports
from .exceptions import CacheKeyNotFound


class Redis:
    DEFAULT_EXPIRATION_TIME = 10800

    def __init__(
        self,
        host: str,
        port: int,
        db: int = 0,
        model: models.Model = apps.get_model("flight.FlightCacheId"),
    ) -> None:
        self.host = host
        self.port = port
        self.db = db
        self.redis_client = redis.Redis(
            host=self.host, port=self.port, db=self.db
        )
        self.model = model

    def has_cache_instance(self, **params):
        cache_id = self.model.objects.filter(**params)
        return cache_id.exists()

    def has_redis_key(self, key):
        return self.redis_client.exists(key)

    def get_cache_instance(self, **params):
        return self.model.objects.get_or_create(**params)[0]

    def create_cache_instance(self, **params):
        return self.model.objects.create(**params)

    def get_cached_instance(self, key):
        if self.has_redis_key(key):
            return json.loads(self.redis_client.get(key))
        raise CacheKeyNotFound

    def get_redis_client(self):
        return self.redis_client

    def get_redis_key(self, instance):
        return str(instance.cache_id)

    def set_redis_key(self, key, data, expiration_time=None):
        self.redis_client.set(str(key), json.dumps(data))
        self.redis_client.expire(
            str(key),
            expiration_time
            if expiration_time is not None
            else self.DEFAULT_EXPIRATION_TIME,
        )

    def set_hash_key(self, key_name, key, value):
        self.redis_client.hmset(str(key_name), {key: json.dumps(value)})
        self.redis_client.expire(str(key_name), 24 * 60 * 60)

    def has_hash_sub_key(self, key_name, key):
        try:
            return self.redis_client.hexists(key_name, key)
        except DataError:
            return None

    def get_hash_key_value(self, key_name, key):
        value = self.redis_client.hmget(key_name, [key])[0]
        return json.loads(value)


###################################
# self.cacheid_obj = CacheId.objects.filter(**self.get_query_params)

# if self.cacheid_obj.exists():
#     self.cacheid_obj = self.cacheid_obj.first()
#     redis_key = str(self.cacheid_obj.cache_id)

#     if redis_client.exists(redis_key):
#         data = redis_client.get(redis_key)
# paginated_data = self.paginator(json.loads(data), limit, offset)
# return Response(status=200, data=paginated_data)
#     else:
#         pass
# else:
#     self.cacheid_obj = CacheId.objects.create(**self.get_query_params)
##################################
