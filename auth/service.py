from abc import abstractmethod, ABC
from datetime import datetime
from uuid import uuid4
from django.utils import timezone

from django.contrib.auth.models import User
from django.db import transaction

from auth.repository import UserProviderRepository
from auth.schema import UserProviderIn, Token
from services.auth_jwt import CustomTokenObtainPairSerializer
from user_provider.models import UserProvider


class ProviderAccountAbstract(ABC):
    repository = UserProviderRepository()
    provider_name=None
    @classmethod
    def get_or_create_user_internal(cls, email) -> User:
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
    def create_user_provider(cls, user_dict) -> UserProvider:
        try:
            user = UserProvider.objects.create(**user_dict)
            return user
        except Exception as e:
            print('create_provider_user - error', e)
            raise e


    @abstractmethod
    def upsert(self, token, profile):
        raise NotImplementedError


class GoogleProvider(ProviderAccountAbstract):
    provider_name = 'google'

    @classmethod
    def upsert(cls, token, profile) -> User:
        provider_id  = profile['sub']

        user_provider_instance = UserProviderIn(
            provider=cls.provider_name,
            provider_account_id=provider_id,
            email=profile['email'],
            email_verified=profile['email_verified'],
            access_token=token['access_token'],
            # refresh_token=token['refresh_token'],
            scopes=token['scope'],
            profile_data=profile,
            expires_in=datetime.fromtimestamp(token['expires_in'], tz=timezone.get_current_timezone()),
            expires_at=datetime.fromtimestamp(token['expires_at'], tz=timezone.get_current_timezone()),
        )

        with transaction.atomic():
            try:
                user_provider: UserProvider = UserProvider.objects.select_for_update().get(provider=cls.provider_name, provider_account_id=provider_id)
                cls.repository.update(user_provider, user_provider_instance.model_dump(exclude_none=True))
                return user_provider.user
            except UserProvider.DoesNotExist:
                user = cls.get_or_create_user_internal(profile['email'])


                payload = {
                    **UserProviderIn.model_validate(user_provider_instance).model_dump(),
                    "user": user
                }
                cls.create_user_provider(payload)
                return user






class AuthService:
    @classmethod
    def get_provider(cls, provider):
        _providers = {
            'google': GoogleProvider
        }
        return _providers[provider]

    @classmethod
    def generate_token(cls, user: User):
        serialized = CustomTokenObtainPairSerializer()
        refresh_token = serialized.get_token(user)
        return  {
            "refresh_token": str(refresh_token),
            "access_token": str(refresh_token.access_token)
        }


