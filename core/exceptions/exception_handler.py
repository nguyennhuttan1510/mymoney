from ninja.errors import ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import APIException


def exception_handler(request, exc):
    if isinstance(exc, APIException):
        return api_exception_handler(request, exc)

    return JsonResponse( {"message": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def api_exception_handler(request, exc: APIException):
    return JsonResponse({
        "success": False,
        "message": str(exc),
        "code": str(exc.default_code)
    }, status= exc.status_code)


def validation_exception_handler(request, exc: ValidationError):
    field_error = {}
    for err in exc.errors:
        loc = ".".join(str(i) for i in err['loc'])
        field_error[loc] = err['msg']
    return JsonResponse({
        "success": False,
        "message": 'validation failed',
        "errors": field_error,
    }, status=422)
