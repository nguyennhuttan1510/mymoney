from typing import Optional, Any
from django.http import HttpRequest
from ninja.security import HttpBearer
from rest_framework_simplejwt.tokens import AccessToken


class JWTAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        try:
            access_token = AccessToken(token)
            return access_token
        except Exception as e:
            return None
