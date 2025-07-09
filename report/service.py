from category.models import Category
from core.schema.service_abstract import ServiceAbstract
from report.patterns.builder import CategoryReportBuilder, ReportBuilder
from report.schema import ReportOut
from transaction.repository import TransactionRepository
from ninja import Query
from transaction.schema import TransactionQueryParams
from transaction.service import TransactionService


class ReportService:
    @staticmethod
    def construct_report_category(builder: ReportBuilder):
        builder.set_category()
        builder.set_wallet()