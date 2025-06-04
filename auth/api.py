from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from ninja import Router
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from auth.schema import LoginSchema, RegisterSchema, RegisterResponseSchema
from core.exceptions.exceptions import BadRequest
from core.schema.response import ResponseSchema, BaseResponse
from services.auth_jwt import JWTAuth

router = Router(tags=['Authentication'])

@router.post("/login")
def login_user(request, payload: LoginSchema):
    user = authenticate(username=payload.username, password=payload.password)
    if not user:
        raise AuthenticationFailed('Invalid username or password')
    login(request, user)
    refresh_token = RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh_token),
        "access_token": str(refresh_token.access_token)
    }


@router.post("/register", response={200: ResponseSchema[RegisterResponseSchema], 400: ResponseSchema})
def register(request, payload: RegisterSchema):
    existed_user = User.objects.filter(username=payload.username).exists()
    if existed_user:
        raise BadRequest("User with this username already exists", 'NOT_FOUND')

    user = User.objects.create_user(**payload.dict())
    return BaseResponse(message="User created successfully", success=True, data=user)


@router.post('/logout', response={200: ResponseSchema}, auth=JWTAuth())
def logout_user(request):
    if not request.user.is_authenticated:
        raise NotAuthenticated('User have not authenticated yet')
    logout(request)
    return BaseResponse(message='Logout successfully', success=True)
