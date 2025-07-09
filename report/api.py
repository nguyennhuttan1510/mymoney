from ninja import Router, Query

from budget.models import Budget
from core.schema.response import ResponseSchema, BaseResponse, SuccessResponse
from report.patterns.builder import CategoryReportBuilder
from report.schema import ReportOut, ResponseBudgetTransaction, ReportIn
from report.service import ReportService
from services.auth_jwt import JWTAuth
from transaction.schema import TransactionQueryParams
from wallet.models import Wallet

router = Router(tags=['Report'], auth=JWTAuth())

@router.get('/reports', response=ResponseSchema[ReportOut])
def report_by(request, filters: Query[ReportIn]):
    builder = CategoryReportBuilder(params=TransactionQueryParams(start_date=filters.start_date, end_date=filters.end_date))
    ReportService.construct_report_category(builder)
    report = builder.build()
    return SuccessResponse(data=report, message='Report category success')

    # wallet = Wallet.objects.get(id=wallet_id, user=request.user)
    # transactions = wallet.transactions.all()
    # wallet_transactions = {
    #     "wallet": wallet,
    #     "transactions": transactions
    # }
    # return wallet_transactions

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
    return BaseResponse(data=budget_transactions, message="Success")