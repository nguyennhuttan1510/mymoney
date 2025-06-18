from http.client import HTTPException
from typing import List

from django.core.exceptions import BadRequest, ObjectDoesNotExist
from ninja import Router, PatchDict, Query
from ninja.errors import HttpError
from rest_framework.exceptions import NotFound

from core.exceptions.exceptions import ValidateError
from core.schema.response import ResponseSchema, BaseResponse, CreateSuccessResponse, BadRequestResponse, \
    SuccessResponse
from services.auth_jwt import JWTAuth
from wallet.schema import WalletOut, WalletIn, WalletParam
from wallet.service import WalletService

router = Router(tags=['Wallet'], auth=JWTAuth())

@router.post('/', response={201: ResponseSchema[WalletOut], 500: ResponseSchema})
def create_wallet(request, payload: WalletIn):
    try:
        wallet = WalletService.create_wallet(user=request.auth, data=payload)
        return CreateSuccessResponse(data=wallet, message="Wallet created successfully")
    except ValueError as e:
        raise ValidateError(e)
    except Exception as e:
        raise HTTPException(f'Create wallet failed - {str(e)}')


@router.get('/', response={200: ResponseSchema[List[WalletOut]], 404: ResponseSchema})
def get_wallets(request, filters: Query[WalletParam]):
    try:
        print('filters', filters.dict())
        wallet = WalletService.repository.get_all_for_user(user_id=request.auth.pk, **filters.dict(exclude_unset=True))
        return SuccessResponse(data=wallet, message="Get wallet successfully")
    except ObjectDoesNotExist:
        raise NotFound("Wallet not found")
    except Exception as e:
        raise HTTPException(str(e))


@router.get('/{int:wallet_id}', response={200: ResponseSchema[WalletOut]})
def get_wallet(request, wallet_id:int):
    try:
        wallet = WalletService.get_wallet(wallet_id=wallet_id, user=request.auth)
        return SuccessResponse(data=wallet, message="Get wallet successfully")
    except ObjectDoesNotExist:
        raise NotFound("Wallet not found")
    except Exception as e:
        raise HTTPException(str(e))


@router.put('/{int:wallet_id}', response={200: ResponseSchema[WalletOut], 400: ResponseSchema, 500: ResponseSchema})
def update_wallet(request, wallet_id:int, payload: PatchDict[WalletIn]):
    try:
        wallet = WalletService.update(wallet_id=wallet_id, data=payload, user=request.auth)
        return SuccessResponse(data=wallet, message="Wallet updated successfully")
    except ObjectDoesNotExist:
        return BadRequestResponse(message="Wallet not found")
    except Exception as e:
        raise HTTPException(str(e))


@router.delete('/{int:wallet_id}', response={200: ResponseSchema})
def delete_wallet(request, wallet_id:int):
    try:
        WalletService.destroy(wallet_id=wallet_id, user=request.auth)
        return SuccessResponse(message=f"Wallet {wallet_id} deleted successfully")
    except ObjectDoesNotExist:
        raise NotFound("Wallet not found")
    except Exception as e:
        raise HTTPException(str(e))