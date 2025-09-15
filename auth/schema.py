from datetime import datetime
from typing import Optional

from django.contrib.auth.models import User
from ninja import Schema
from pydantic import Field, BaseModel


class LoginSchema(Schema):
    username: str = Field(default='admin')
    password: str = Field(default='o0i9u8y7')

class RegisterSchema(LoginSchema, Schema):
    email: str
    last_name: Optional[str] = ''
    first_name: Optional[str] = ''

class Token(Schema):
    access_token: str
    refresh_token: str

class RegisterResponseSchema(Schema):
    username: str
    email: str

class UserProviderIn(BaseModel):
    provider: str
    provider_account_id: str
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: datetime
    expires_at: datetime
    scopes: Optional[str] = None
    profile_data: Optional[dict] = None
    email: str
    email_verified: bool



