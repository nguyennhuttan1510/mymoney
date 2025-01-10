import json
from typing import Generic, TypeVar, Optional

from ninja import Schema

T = TypeVar('T')

class ResponseSchema(Schema, Generic[T]):
    data: Optional[T] = None
    message: str = None
    success: bool = True

class Response:
    def __init__(self, data=None, message=None, success=True):
        self.data = data
        self.message = message
        self.success = success


