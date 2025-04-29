import json

def auth_client(client, token):
    def wrapper(method, path, data=None):
        return getattr(client, method)(
            path,
            data=json.dumps(data) if data else None,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )
    return wrapper