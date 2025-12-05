import random
import time

from django.core.cache import cache

from core.cache import redis
from core.cache.redis import redis_client


def _now():
    return int(time.time())


class Cache:
    def __init__(self, base_ttl=60, soft_ttl=50, jitter=20):
        self.base_ttl=base_ttl
        self.soft_ttl=soft_ttl
        self.jitter=jitter

    # def get(self, key):
    #     cached  = cache.get(key)
    #     if not cached:
    #         # with redis.lock()



    def set(self, key, data):
        hard_ttl = self.base_ttl + random.randint(0, self.jitter)
        # payload = {
        #     "data": data,
        #     "expires_at": _now() + self.soft_ttl
        # }
        cache.set(key, data, self.base_ttl)
