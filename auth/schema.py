from typing import Optional

from ninja import Schema

class LoginSchema(Schema):
    username: str
    password: str

class RegisterSchema(LoginSchema, Schema):
    email: str
    last_name: Optional[str] = ''
    first_name: Optional[str] = ''


class RegisterResponseSchema(Schema):
    username: str
    email: str


