from ninja import Router, Query

from budget.models import Budget
from core.schema.response import ResponseSchema, SuccessResponse
from report.patterns.builder import CategoryReportBuilder
from report.schema import ReportOut, ReportQuery
from report.service import ReportService
from services.auth_jwt import JWTAuth
from transaction.schema import TransactionQuery

router = Router(tags=['Report'], auth=JWTAuth())

@router.get('/reports', response=ResponseSchema[ReportOut])
def report_by(request, query: Query[ReportQuery]):
    builder = CategoryReportBuilder(params=TransactionQuery(**query.model_dump(exclude_none=True)))
    report = builder.set_category().set_wallet().build()
    return SuccessResponse(data=report.model_dump(), message='Report category success')

@router.get('/reports/generate', response=ResponseSchema[ReportOut])
def generate_report(request, query: Query[ReportQuery]):
    builder = CategoryReportBuilder(params=TransactionQuery(**query.model_dump(exclude_none=True)))
    return ReportService.handle_report(builder, user=request.auth)
