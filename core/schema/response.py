from typing import Generic, TypeVar, Optional
from ninja import Schema
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_201_CREATED

T = TypeVar('T')


class ResponseSchema(Schema, Generic[T]):
    data: Optional[T] = None
    message: str = None
    success: bool = True

    class Config:
        from_attributes = True


class BaseResponse(Generic[T]):
    http_status: int = None
    success: bool = None
    message: str = None

    def __new__(cls, message: Optional[str] = None, data: Optional[T] = None, success: Optional[bool] = None):
        if cls.http_status is None:
            raise NotImplementedError("BaseResponse cannot be used directly — subclass required.")
        return cls.http_status, ResponseSchema(data=data, message=message or cls.message,
                                      success=success or cls.success)


class SuccessResponse(BaseResponse):
    http_status = HTTP_200_OK
    success = True
    message = 'Success'


class CreateSuccessResponse(BaseResponse):
    http_status = HTTP_201_CREATED
    success = True
    message = 'Create success'


class BadRequestResponse(BaseResponse):
    http_status = HTTP_400_BAD_REQUEST
    success = False
    message = 'Bad request'


class NotFoundResponse(BaseResponse):
    http_status = HTTP_404_NOT_FOUND
    success = False
    message = 'Not found'
