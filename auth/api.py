from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from ninja import Router
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotFound, ValidationError, NotAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from auth.schema import LoginSchema, RegisterSchema, RegisterResponseSchema
from core.exceptions.api_exception import HttpBadRequestException
from core.schema.response import ResponseSchema, Response
from services.auth_jwt import JWTAuth

router = Router(tags=['Authentication'])

@router.post("/login")
def login_user(request, data: LoginSchema):
    user = authenticate(username=data.username, password=data.password)
    if not user:
        raise AuthenticationFailed('Invalid username or password')
    login(request, user)
    refresh_token = RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh_token),
        "access_token": str(refresh_token.access_token)
    }

@router.post("/register", response=ResponseSchema[RegisterResponseSchema])
def register(request, payload: RegisterSchema):
    existed_user = User.objects.filter(username=payload.username).exists()
    if existed_user:
        raise HttpBadRequestException("User with this username already exists")

    user = User.objects.create_user(**payload.dict())
    return Response(message="User created successfully", success=True, data=user)

@router.post('/logout', response={200: ResponseSchema}, auth=JWTAuth())
def logout_user(request):
    if not request.user.is_authenticated:
        raise NotAuthenticated('User have not authenticated yet')
    logout(request)
    return Response(message='Logout successfully', success=True)
