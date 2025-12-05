from abc import abstractmethod, ABC
from datetime import datetime
from typing import Dict, Type, Any
from uuid import uuid4

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.cache import cache
from django.db.models import QuerySet, Q
from django.utils import timezone

from django.contrib.auth.models import User
from django.db import transaction
from django.utils.dateparse import parse_datetime
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from auth.repository import UserProviderRepository
from auth.schema import UserProviderIn, Token, PayloadToken, UserIn
from core.cache.redis import redis_client as r
from core.exceptions.exceptions import BadRequest
from core.exceptions.session_exception import SessionException, SessionInactive, SessionInvalid, SessionExpired
from session.models import Session
from user_provider.models import UserProvider
from services.oauth import oauth, cfg
from utils.query_builder import QueryBuilder


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User, payload: PayloadToken | None = None) -> Token:
        token = super().get_token(user)

        # Add custom claims from payload if provided
        if payload:
            for key, value in payload.model_dump().items():
                token[key] = str(value)

        return token


class ProviderAccountAbstract(ABC):
    provider_name = None

    @abstractmethod
    def login(self, request):
        raise NotImplementedError

    @abstractmethod
    def get_token(self, request) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_user_provider(self, response_access: dict[str, Any]) -> UserProviderIn:
        raise NotImplementedError


class GoogleProvider(ProviderAccountAbstract):
    provider_name = 'google'

    def login(self, request):
        redirect_uri = cfg["redirect_uri"]
        return oauth.google.authorize_redirect(request, redirect_uri)

    def get_token(self, request):
        return oauth.google.authorize_access_token(request)

    def get_user_provider(self, response_access) -> UserProviderIn:
        return UserProviderIn(
            provider=self.provider_name,
            provider_account_id=response_access['userinfo']['sub'],
            email=response_access['userinfo']['email'],
            email_verified=response_access['userinfo']['email_verified'],
            access_token=response_access['access_token'],
            # refresh_token=token['refresh_token'],
            scopes=response_access['scope'],
            profile_data=response_access['userinfo'],
            expires_in=datetime.fromtimestamp(response_access['expires_in'], tz=timezone.get_current_timezone()),
            expires_at=datetime.fromtimestamp(response_access['expires_at'], tz=timezone.get_current_timezone()),
        )


class AuthService:
    repository_provider = UserProviderRepository()

    @classmethod
    def get_provider(cls, provider) -> Type[ProviderAccountAbstract]:
        _providers = {
            'google': GoogleProvider
        }
        return _providers[provider]

    @classmethod
    def upsert(cls, payload: UserProviderIn) -> User:
        with transaction.atomic():
            try:
                instance: UserProvider = cls._get_user_provider(payload)
                cls._update_user_provider(instance, payload.model_dump())
                return instance.user
            except UserProvider.DoesNotExist:
                user = cls._get_or_create_user_internal(payload.email)
                payload = {
                    **UserProviderIn.model_validate(payload).model_dump(),
                    "user": user
                }
                cls._create_user_provider(payload)
                return user

    @classmethod
    def _get_or_create_user_internal(cls, email) -> User:
        try:
            return User.objects.get(Q(email__iexact=email) | Q(username=email))
        except User.DoesNotExist:
            return cls._create_user(UserIn(username=email or uuid4(), email=email or ""))

    @classmethod
    def _validate_create_user(cls, payload: UserIn):
        existed_user = User.objects.filter(Q(username=payload.username) | Q(email=payload.email)).exists()
        if existed_user:
            raise BadRequest("username or email already exists", 'NOT_FOUND')

    @classmethod
    def _create_user(cls, payload: UserIn):
        return User.objects.create_user(**payload.dict())

    @classmethod
    def _create_session(cls, payload) -> Session:
        return Session.objects.create(**payload)

    @classmethod
    def create_user(cls, payload: UserIn):
        cls._validate_create_user(payload)
        return cls._create_user(payload)

    @classmethod
    def validate_session(cls, session_id: str, user) -> Session:
        if not session_id:
            raise SessionException('Session id is required')

        try:
            session_cached = cache.get(cls._create_session_key(user, session_id))
            if not session_cached:
                raise SessionException('Not found in cache')

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

    @classmethod
    def generate_token(cls, user: User, session: Session):
        payload = PayloadToken(
            session_id=session.session_id,
            email=user.email,
        )

        serialized = CustomTokenObtainPairSerializer()
        refresh_token = serialized.get_token(user, payload)

        return {
            "refresh_token": str(refresh_token),
            "access_token": str(refresh_token.access_token)
        }

    @classmethod
    def _create_user_provider(cls, user_dict) -> UserProvider:
        try:
            user = cls.repository_provider.create(**user_dict)
            return user
        except Exception as e:
            raise e

    @classmethod
    def _get_user_provider(cls, user_provider: UserProviderIn):
        return cls.repository_provider.model.objects.select_for_update().get(provider=user_provider.provider,
                                                                             provider_account_id=user_provider.provider_account_id)

    @classmethod
    def _update_user_provider(cls, instance, user_dict) -> UserProvider:
        try:
            user = cls.repository_provider.update(instance, user_dict)
            return user
        except Exception as e:
            print('Update user provider error', e)
            raise e

    @classmethod
    def _revoke_session(cls, query_builder: QueryBuilder, note="revoked due to new login"):
        Session.objects.filter(query_builder.build()).update(is_active=False, note=note, revoked_at=datetime.now())

    @classmethod
    def _create_session_key(cls, user, session_id):
        return f"session:{user.id}:{session_id}"

    @classmethod
    def _cache_session(cls, key, session: Session):
        payload = {
            "session_id": str(session.session_id),
            "is_active": session.is_active,
            "expires_at": session.expires_at.isoformat()
        }
        cache.set(key, payload, timeout=settings.SESSION_EXPIRE_MINUTES)

    @classmethod
    def _revoke_cache_session(cls, keys):
        cache.delete_many(keys)

    @classmethod
    def _delete_pattern(cls, pattern):
        cursor = 0
        while True:
            cursor, keys = r.scan(cursor=cursor, match=f"myapp:1:{pattern}", count=2000)
            if keys:
                r.unlink(*keys)  # non-blocking delete
            if cursor == 0:
                break

    @classmethod
    def login_process(cls, payload, request):
        #Step 1: validate user
        user = authenticate(username=payload.username, password=payload.password)
        if not user:
            raise AuthenticationFailed('Invalid username or password')
        login(request, user)

        #Step 2: Check session existing and disabled
        query_builder = QueryBuilder().add_condition("user", user).add_condition("is_active", True)
        cls._revoke_session(query_builder)
        cls._delete_pattern(f"session:{user.id}:*")

        #Step 3: Create new session
        session = cls._create_session({"user": user, "user_agent": request.META.get("HTTP_USER_AGENT", "")})

        #Step 4: Cache
        session_key = cls._create_session_key(user, str(session.session_id))
        cls._cache_session(session_key, session)

        return cls.generate_token(user, session=session)

    @classmethod
    def provider_onboard_process(cls, provider_name, request):
        provider_class = cls.get_provider(provider_name)
        provider = provider_class()

        token = provider.get_token(request)
        print('token', token)
        provider_in = provider.get_user_provider(token)

        user = cls.upsert(provider_in)
        session = cls._create_session({"user": user, "user_agent": request.META.get("HTTP_USER_AGENT", "")})
        return cls.generate_token(user, session=session)
