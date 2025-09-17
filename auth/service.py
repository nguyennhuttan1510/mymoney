from abc import abstractmethod, ABC
from datetime import datetime
from typing import Dict, Type, Any
from uuid import uuid4

from django.contrib.auth import authenticate, login
from django.utils import timezone

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from auth.repository import UserProviderRepository
from auth.schema import UserProviderIn, Token, PayloadToken
from session.models import Session
from user_provider.models import UserProvider
from services.oauth import oauth, cfg



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User, payload: PayloadToken|None = None) -> Token:
        token = super().get_token(user)

        # Add custom claims from payload if provided
        if payload:
            for key, value in payload.model_dump().items():
                token[key] = str(value)

        return token


class ProviderAccountAbstract(ABC):
    provider_name=None

    @abstractmethod
    def login(self, request):
        raise NotImplemented

    @abstractmethod
    def get_token(self, request) -> dict[str, Any]:
        raise NotImplemented

    @abstractmethod
    def get_user_provider(self, response_access: dict[str, Any]) -> UserProviderIn:
        raise NotImplemented


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
        uuid = uuid4()
        if email:
            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                user = User.objects.create_user(username=email, email=email)
        else:
            user = User.objects.create_user(username=uuid, email=email or "")
        return user

    @classmethod
    def _create_session(cls, payload) -> Session:
        return Session.objects.create(**payload)

    @classmethod
    def validate_session(cls, session_id: str) -> Session:
        if not session_id:
            raise Exception('Session id is required')

        try:
            session = Session.objects.get(session_id=session_id)
        except Session.DoesNotExist:
            raise Exception('Session not found')

        if not session.is_active:
            raise Exception('Session inactive')

        if session.expires_at >= datetime.now():
            raise Exception('Session expired')

        return session

    @classmethod
    def generate_token(cls, user: User, session: Session = None):
        session = session or cls._create_session({"user":user})
        payload = PayloadToken(
            session_id=session.session_id,
            email=user.email,
        )

        serialized = CustomTokenObtainPairSerializer()
        refresh_token = serialized.get_token(user, payload)

        return  {
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
        return cls.repository_provider.model.objects.select_for_update().get(provider=user_provider.provider_name, provider_account_id=user_provider.provider_account_id)

    @classmethod
    def _update_user_provider(cls, instance, user_dict) -> UserProvider:
        try:
            user = cls.repository_provider.update(instance, **user_dict)
            return user
        except Exception as e:
            print('Update user provider error', e)
            raise e

    @classmethod
    def login_process(cls, payload, request):
        user = authenticate(username=payload.username, password=payload.password)
        if not user:
            raise AuthenticationFailed('Invalid username or password')
        login(request, user)

        other_session = Session.objects.filter(user=user, is_active=True)
        other_session.update(is_active=False, revoked_at=timezone.now(), note='revoked due to new login')

        session = cls._create_session({"user":user, "user_agent": request.META.get("HTTP_USER_AGENT", "")})

        return cls.generate_token(user, session=session)

    @classmethod
    def provider_onboard_process(cls, provider_name, request):
        Provider = cls.get_provider(provider_name)
        instance_provider = Provider()

        token = instance_provider.get_token(request)
        print('token', token)
        provider_in = instance_provider.get_user_provider(token)

        user = cls.upsert(provider_in)

        return cls.generate_token(user)
