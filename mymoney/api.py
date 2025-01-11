from ninja import NinjaAPI
from ninja.errors import HttpError
from rest_framework import status
from rest_framework.exceptions import APIException

api = NinjaAPI()

@api.exception_handler(Exception)
def handle_server_error(request, exc):
    if isinstance(exc, APIException):
        return api.create_response(request, {"message": str(exc)}, status=exc.status_code)
    return api.create_response(request, {"message": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

api.add_router('/transaction', 'transaction.api.router')
api.add_router('/auth', 'auth.api.router')
api.add_router('/category', 'category.api.router')
