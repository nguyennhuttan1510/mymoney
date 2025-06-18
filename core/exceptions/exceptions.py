from rest_framework import status
from rest_framework.exceptions import APIException

class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid input.'
    default_code = 'invalid'

class ServerError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Server Error (500).'
    default_code = 'server_error'

class ValidateError(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = 'Invalid input.'
    default_code = 'invalid'



