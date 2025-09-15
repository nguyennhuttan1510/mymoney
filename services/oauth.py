from authlib.integrations.django_client import OAuth
from django.conf import settings

oauth = OAuth()
cfg = settings.OAUTH_PROVIDERS["google"]
oauth.register(
    name="google",
    client_id=cfg["client_id"],
    client_secret=cfg["client_secret"],
    access_token_url=cfg["access_token_url"],
    authorize_url=cfg["authorize_url"],
    client_kwargs={"scope": cfg["scope"]},
    response_type="code",
    server_metadata_url=cfg["server_metadata_url"]

)