import uuid
import time
from abc import ABC, abstractmethod
from sys import prefix
from typing import Dict, Any, Type

from core.cache.key_generator import KeyGenerateDefault
from core.cache.redis import RedisCache
from core.exceptions.session_exception import SessionException, SessionInactive, SessionInvalid, SessionExpired
from utils.query_builder import QueryBuilder
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from session.models import Session
from django.core.cache import cache

class CachingSession(RedisCache):
    def __init__(self):
        self.prefix = "session"
        self.key = KeyGenerateDefault()
        super().__init__()

    def make_key(self, user_id, session_id):
        return self.key.generate(self.prefix, str(user_id), session_id)



class SessionService:
    cache = CachingSession()

    @classmethod
    def create_session(cls, user_id, request):
        ttl = 3600
        session_id = str(uuid.uuid4())
        data = {
            "user_id": user_id,
            "session_id": session_id,
            "user_agent": request.META.get("HTTP_USER_AGENT", ""),
            "created_at": time.time(),
            "expired_at": time.time() + ttl,
        }
        key = cls.cache.make_key(user_id, session_id)
        cls.cache.set(key, data, ttl)
        return session_id

    @classmethod
    def delete_all_session(cls, user_id):
        cls.cache.clear(f"{cls.cache.prefix}:{user_id}:*")

    @classmethod
    def validate_session(cls, user_id, session_id):
        key = cls.cache.make_key(user_id, session_id)
        cached = cls.cache.get(key)
        if not cached:
            return SessionExpired()
        return cached




    # @classmethod
    # def validate_session(cls, session_id: str) -> Session:
    #     if not session_id:
    #         raise SessionException('Session id is required')
    #
    #     try:
    #         session_cached = cache.get(cls._create_session_key(user, session_id))
    #         if not session_cached:
    #             raise SessionException('Not found session in cache')
    #
    #         if not session_cached["is_active"]:
    #             raise SessionInactive()
    #
    #         if not session_cached['expires_at']:
    #             raise SessionInvalid('Session not found expired_at')
    #
    #         if parse_datetime(session_cached['expires_at']) <= timezone.now():
    #             raise SessionExpired()
    #
    #
    #     except SessionException as e:
    #         query_builder = QueryBuilder().add_condition("session_id", session_id)
    #         cls._revoke_session(query_builder, str(e))
    #         raise e
    #
    #     return session_cached
