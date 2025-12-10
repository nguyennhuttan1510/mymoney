from core.exceptions.session_exception import SessionException, SessionInactive, SessionInvalid, SessionExpired
from utils.query_builder import QueryBuilder
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from session.models import Session
from django.core.cache import cache


class SessionService:
    @classmethod
    def _revoke_session(cls, query_builder: QueryBuilder, note="revoked due to new login"):
        Session.objects.filter(query_builder.build()).update(is_active=False, note=note, revoked_at=timezone.now())


    @classmethod
    def validate_session(cls, session_id: str, user) -> Session:
        if not session_id:
            raise SessionException('Session id is required')

        try:
            session_cached = cache.get(cls._create_session_key(user, session_id))
            if not session_cached:
                raise SessionException('Not found session in cache')

            if not session_cached["is_active"]:
                raise SessionInactive()

            if not session_cached['expires_at']:
                raise SessionInvalid('Session not found expired_at')

            if parse_datetime(session_cached['expires_at']) <= timezone.now():
                raise SessionExpired()


        except SessionException as e:
            query_builder = QueryBuilder().add_condition("session_id", session_id)
            cls._revoke_session(query_builder, str(e))
            raise e

        return session_cached
