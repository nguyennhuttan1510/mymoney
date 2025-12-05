from typing import Optional, Any

from django.contrib.auth.models import User
from django.http import HttpRequest
from ninja.security import HttpBearer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token

from auth.schema import PayloadToken
from auth.service import AuthService
from core.exceptions.session_exception import SessionException
from session.models import Session


class JWTAuth(HttpBearer):
    def authenticate(self, request: Request, token) -> Optional[Any]:
        jwt_auth = JWTAuthentication()
        try:
            user, validated_token = jwt_auth.authenticate(request)
            print('session_id', validated_token['session_id'])
            AuthService.validate_session(validated_token['session_id'], user)
            return user

        except SessionException as e:
            raise e

        except Exception as e:
            raise AuthenticationFailed(str(e) or 'Invalid token')
