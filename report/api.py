from ninja import Router

from core.schema.response import ResponseSchema, Response
from report.schema import ReportWalletTransaction
from services.auth_jwt import JWTAuth
from wallet.models import Wallet

router = Router(tags=['Report'], auth=JWTAuth())

@router.get('/wallet-transactions/{int:wallet_id}', response=ReportWalletTransaction)
def get_wallet_transactions(request, wallet_id: int):
    wallet = Wallet.objects.get(id=wallet_id, user=request.user)
    transactions = wallet.transactions.all()
    wallet_transactions = {
        "wallet": wallet,
        "transactions": transactions
    }
    return wallet_transactions