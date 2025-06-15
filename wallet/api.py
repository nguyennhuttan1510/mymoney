from http.client import HTTPException

from ninja import Router, PatchDict
from rest_framework.exceptions import NotFound

from core.schema.response import ResponseSchema, BaseResponse, CreateSuccessResponse
from services.auth_jwt import JWTAuth
from wallet.models import Wallet
from wallet.schema import WalletOut, WalletIn
from wallet.service import WalletService

router = Router(tags=['Wallet'], auth=JWTAuth())

@router.post('/', response={201: ResponseSchema[WalletOut], 500: ResponseSchema})
def create_wallet(request, payload: WalletIn):
    try:
        wallet = WalletService.create_wallet(user=request.user, data=payload)
        return CreateSuccessResponse(data=wallet, message="Wallet created successfully")
    except Exception as e:
        raise HTTPException(f'Create wallet failed - {str(e)}')


@router.get('/{int:wallet_id}', response=ResponseSchema[WalletOut])
def get_wallet(request, wallet_id:int):
    try:
        wallet = Wallet.objects.get(user=request.user, id=wallet_id)
        return BaseResponse(data=wallet, message="Get wallet successfully")
    except Wallet.DoesNotExist:
        raise NotFound("Wallet not found")
    except Exception as e:
        raise HTTPException(str(e))


@router.put('/{int:wallet_id}', response=ResponseSchema[WalletOut])
def update_wallet(request, wallet_id:int, item: PatchDict[WalletIn]):
    try:
        wallet = Wallet.objects.get(user=request.user, id=wallet_id)
        for key, value in item.items():
            if value is not None:
                setattr(wallet, key, value)
        return BaseResponse(data=wallet, message="Wallet updated successfully")
    except Wallet.DoesNotExist:
        raise NotFound("Wallet not found")
    except Exception as e:
        raise HTTPException(str(e))


@router.delete('/{int:wallet_id}', response=ResponseSchema[WalletOut])
def delete_wallet(request, wallet_id:int):
    try:
        wallet = Wallet.objects.get(user=request.user, id=wallet_id)
        wallet.delete()
        return BaseResponse(data=wallet, message="Wallet deleted successfully")
    except Wallet.DoesNotExist:
        raise NotFound("Wallet not found")
    except Exception as e:
        raise HTTPException(str(e))