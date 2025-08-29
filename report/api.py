from ninja import Router, Query

from budget.models import Budget
from core.schema.response import ResponseSchema, SuccessResponse
from report.patterns.builder import CategoryReportBuilder
from report.schema import ReportOut, ResponseBudgetTransaction, ReportIn
from report.service import ReportService
from services.auth_jwt import JWTAuth
from transaction.schema import TransactionQueryParams

router = Router(tags=['Report'], auth=JWTAuth())

@router.get('/reports', response=ResponseSchema[ReportOut])
def report_by(request, filters: Query[ReportIn]):
    builder = CategoryReportBuilder(params=TransactionQueryParams(start_date=filters.start_date, end_date=filters.end_date))
    ReportService.construct_report_category(builder)
    report = builder.build()
    return SuccessResponse(data=report.model_dump(), message='Report category success')

@router.get('/reports/generate', response=ResponseSchema[ReportOut])
def generate_report(request, filters: Query[ReportIn]):
    builder = CategoryReportBuilder(params=TransactionQueryParams(start_date=filters.start_date, end_date=filters.end_date))
    ReportService.construct_report_category(builder)
    return ReportService.handle_report(builder, user=request.auth)

@router.get('/budget-transactions/{int:budget_id}', response=ResponseSchema[ResponseBudgetTransaction])
def get_budget_transactions(request, budget_id: int):
    result = ReportService.report_by_budget(budget_id)
    return SuccessResponse(data=result)