from typing import List

from ninja import Router

from core.schema.response import ResponseSchema, SuccessResponse, BadRequestResponse
from services.auth_jwt import JWTAuth
from user.service import UserService
from wallet.schema import WalletOut
from wallet.service import WalletService

router = Router(tags=['User'], auth=JWTAuth())

@router.get('/{int:user_id}/wallets', response={200: ResponseSchema[List[WalletOut]]})
def get_wallet_user(request, user_id:int):
    try:
        wallets = UserService.get_wallets_user(user_id)
        return SuccessResponse(data=wallets, message="Get wallets of user success")
    except Exception as e:
        return BadRequestResponse(message=str(e))