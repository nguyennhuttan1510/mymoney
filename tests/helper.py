import json

from rest_framework_simplejwt.tokens import RefreshToken


def generate_token(user):
    refresh_token = RefreshToken.for_user(user=user)
    return refresh_token.access_token


def auth_client(client, user):
    token = generate_token(user)

    def wrapper(method, path, data=None):
        print(f"[DEBUG] HTTP method: {method.upper()} - URL: {path}")
        return getattr(client, method)(
            path,
            data=data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )

    return wrapper
