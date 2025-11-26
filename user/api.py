from typing import List

from ninja import Router

from asset.schema import AssetList
from budget.schema import BudgetListOut
from core.schema.response import ResponseSchema, SuccessResponse, BadRequestResponse
from services.auth_jwt import JWTAuth
from user.service import UserService
from wallet.schema import WalletOut, WalletListOut
from wallet.service import WalletService

router = Router(tags=['User'], auth=JWTAuth())

@router.get('/{int:user_id}/wallets', response={200: ResponseSchema[WalletListOut]})
def get_wallet_user(request, user_id:int):
    try:
        wallets = UserService.get_wallets(user_id)
        return SuccessResponse(data=wallets, message="Get wallets of user success")
    except Exception as e:
        return BadRequestResponse(message=str(e))


@router.get('/{int:user_id}/budgets', response={200: ResponseSchema[BudgetListOut], 400: ResponseSchema})
def get_budgets_user(request, user_id:int):
    try:
        budgets = UserService.get_budgets(user_id)
        return SuccessResponse(data=budgets, message="Get budgets of user success")
    except Exception as e:
        return BadRequestResponse(message=str(e))


@router.get('/{int:user_id}/assets', response={200:ResponseSchema[AssetList], 400: ResponseSchema})
def get_assets_user(request, user_id:int):
    try:
        assets = UserService.get_assets(user_id)
        return SuccessResponse(data=assets, message='Get assets of user success')
    except Exception as e:
        return BadRequestResponse(message=str(e))