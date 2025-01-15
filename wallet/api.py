from http.client import HTTPException

from ninja import Router, PatchDict
from rest_framework.exceptions import NotFound

from core.schema.response import ResponseSchema, Response
from services.auth_jwt import JWTAuth
from wallet.models import Wallet
from wallet.schema import WalletSchema

router = Router(tags=['Wallet'], auth=JWTAuth())

@router.post('/', response=ResponseSchema[WalletSchema])
def create_wallet(request, payload: WalletSchema):
    wallet = Wallet.objects.create(user=request.user,**payload.dict())
    return Response(data=wallet, message="Wallet created successfully")


@router.get('/{int:wallet_id}', response=ResponseSchema[WalletSchema])
def get_wallet(request, wallet_id:int):
    try:
        wallet = Wallet.objects.get(user=request.user, id=wallet_id)
        return Response(data=wallet, message="Get wallet successfully")
    except Wallet.DoesNotExist:
        raise NotFound("Wallet not found")
    except Exception as e:
        raise HTTPException(str(e))


@router.put('/{int:wallet_id}', response=ResponseSchema[WalletSchema])
def update_wallet(request, wallet_id:int, item: PatchDict[WalletSchema]):
    try:
        wallet = Wallet.objects.get(user=request.user, id=wallet_id)
        for key, value in item.items():
            if value is not None:
                setattr(wallet, key, value)
        return Response(data=wallet, message="Wallet updated successfully")
    except Wallet.DoesNotExist:
        raise NotFound("Wallet not found")
    except Exception as e:
        raise HTTPException(str(e))


@router.delete('/{int:wallet_id}', response=ResponseSchema[WalletSchema])
def delete_wallet(request, wallet_id:int):
    try:
        wallet = Wallet.objects.get(user=request.user, id=wallet_id)
        wallet.delete()
        return Response(data=wallet, message="Wallet deleted successfully")
    except Wallet.DoesNotExist:
        raise NotFound("Wallet not found")
    except Exception as e:
        raise HTTPException(str(e))