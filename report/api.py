from ninja import Router

from budget.models import Budget
from core.schema.response import ResponseSchema, Response
from report.schema import ReportWalletTransaction, ResponseBudgetTransaction
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

@router.get('/budget-transactions/{int:budget_id}', response=ResponseSchema[ResponseBudgetTransaction])
def get_budget_transactions(request, budget_id: int):
    budget = Budget.objects.get(pk=budget_id)
    transactions = budget.transactions.all()

    sum_transactions = sum([transaction.amount for transaction in transactions])

    budget_transactions = {
        "budget": budget,
        "transactions": transactions,
        "spent": sum_transactions,
        "remaining": budget.amount - sum_transactions,
        "percentage_spent": (sum_transactions / budget.amount) * 100 if budget.amount > 0 else 0,
        "percentage_remaining": ((budget.amount - sum_transactions) / budget.amount) * 100 if budget.amount > 0 else 100,
    }
    return Response(data=budget_transactions, message="Success")