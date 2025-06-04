from abc import ABC
from typing import Generic, TypeVar, Optional, Any
from ninja import Schema
from pydantic import BaseModel
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_201_CREATED

T = TypeVar('T')

class ResponseSchema(Schema, Generic[T]):
    data: Optional[T] = None
    message: str = None
    success: bool = True


class BaseResponse(ABC):
    http_status: int
    success: bool
    message: Optional[str] = None

    def __init__(self, message: str = None, data: Optional[Any] = None):
        self.data = data
        if message:
            self.message = message

    def to_response(self):
        return self.http_status, self

class SuccessResponse(BaseResponse):
    http_status = HTTP_200_OK
    success = True
    message = 'Success'

class CreateSuccessResponse(BaseResponse):
    http_status = HTTP_201_CREATED
    success = True
    message = 'Create success'

class ResponseAPI:
    def __new__(cls, obj: BaseResponse ):
        return obj.to_response()
