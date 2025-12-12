import json
import threading
from abc import ABC, abstractmethod
from typing import Type

from django.core.serializers.json import DjangoJSONEncoder

import redis
from core.cache.exception import ConnectError
from core.cache.interface import CacheConnect, CacheStrategy, KeyGenerator, Serializer
from core.cache.serializer import JsonSerializer


class RedisSingleton(CacheConnect):
    _instance = None
    _lock = threading.Lock()
    _host = None
    _port = None
    @classmethod
    def init(cls, host='10.91.10.19', port=6379) -> Type['RedisSingleton']:
        cls._host = host
        cls._port = port
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    print('redis is connecting... ')
                    cls._instance = redis.Redis(host=host, port=port, decode_responses=True)
                    print('connection redis', cls._instance.ping())
        return cls

    @classmethod
    def get_client(cls) -> redis.Redis:
        if not cls._instance:
            raise ConnectError(f"Not found instance redis with {cls._host}:{cls._port}")
        return cls._instance



class RedisCache(CacheStrategy):
    def __init__(self, serializer: Serializer = JsonSerializer()):
        self.client = RedisSingleton.init().get_client()
        self.serializer = serializer

    @abstractmethod
    def make_key(self, *args, **kwargs):
        pass

    def get(self, key: str):
        data = self.client.get(key)
        if not data:
            return None
        return self.serializer.deserialize(data)

    def set(self, key, value, ttl):
        data = self.serializer.serialize(value)
        return self.client.set(key, data, ex=ttl)

    def delete(self, key: str):
        if not key:
            return None
        return self.client.delete(key)

    def scan(self, pattern: str):
        cursor = 0
        keys = []
        while True:
            cursor, batch = self.client.scan(cursor=cursor, match=pattern)
            keys.extend(batch)
            if cursor == 0:
                break
        return keys

    def existed(self, key:str):
        pass

    def clear(self, pattern:str):
        keys = self.scan(pattern)
        if not keys:
            return None
        self.delete(*keys)

    def get_or_set(self, key:str, ttl, fetch):
        cached = self.get(key)
        if not cached:
            data = fetch()
            self.set(key, data, ttl)
            return data
        return cached

