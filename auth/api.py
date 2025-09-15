from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from ninja import Router
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from auth.service import AuthService
from services.oauth import oauth, cfg

from auth.schema import LoginSchema, RegisterSchema, RegisterResponseSchema, Token
from core.exceptions.exceptions import BadRequest
from core.schema.response import ResponseSchema, BaseResponse, SuccessResponse
from services.auth_jwt import JWTAuth, CustomTokenObtainPairSerializer

router = Router(tags=['Authentication'])

@router.post("/login", response={200: ResponseSchema, 400: ResponseSchema})
def login_user(request, payload: LoginSchema):
    user = authenticate(username=payload.username, password=payload.password)
    if not user:
        raise AuthenticationFailed('Invalid username or password')
    login(request, user)
    res = AuthService.generate_token(user)
    return SuccessResponse(data=res)


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


@router.get('/google/login', response={200: ResponseSchema})
def provider_login(request):
    redirect_uri = cfg["redirect_uri"]
    return oauth.google.authorize_redirect(request, redirect_uri)



@router.get('/google/callback', response={200: ResponseSchema[Token]})
def provider_callback(request):
    token = oauth.google.authorize_access_token(request)
    print('token', token)
    provider = AuthService.get_provider('google')
    user_internal = provider.upsert(token, token['userinfo'])
    internal_token = AuthService.generate_token(user_internal)
    # return SuccessResponse(data=internal_token)
    return redirect(f'https://www.youtube.com/watch?v=8q2lBNbdsEo&list=RD8q2lBNbdsEo&start_radio=1&token={internal_token["access_token"]}')
