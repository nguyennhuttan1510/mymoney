from category.models import Category
from core.schema.service_abstract import ServiceAbstract
from report.generator.wallet import TransactionReportGenerator
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

    @staticmethod
    def handle_report(builder: ReportBuilder, user):
        generator = TransactionReportGenerator(builder=builder, user=user)
        file = generator.generate()
        return file

