from typing import Optional, Any

from django.contrib.auth.models import User
from django.http import HttpRequest
from ninja.security import HttpBearer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token


class JWTAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token) -> Optional[Any]:
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)
            return user

        except Exception as e:
            raise AuthenticationFailed('Invalid token')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User) -> Token:
        token = super().get_token(user)
        token['email'] = user.email
        return token
