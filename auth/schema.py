from typing import Optional

from ninja import Schema
from pydantic import Field


class LoginSchema(Schema):
    username: str = Field(default='admin')
    password: str = Field(default='o0i9u8y7')

class RegisterSchema(LoginSchema, Schema):
    email: str
    last_name: Optional[str] = ''
    first_name: Optional[str] = ''


class RegisterResponseSchema(Schema):
    username: str
    email: str


