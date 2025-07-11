from datetime import datetime

from django.http import HttpResponse

from report.patterns.builder import ReportBuilder
from report.patterns.report_strategy import BaseReportStrategy
from openpyxl import Workbook

from report.patterns.report_template_method import TransactionReportTemplate
from report.schema import ReportOut
from transaction.models import Transaction
from transaction.repository import TransactionRepository


class TransactionReportGenerator(BaseReportStrategy):
    def __init__(self, builder: ReportBuilder[ReportOut], user):
        super().__init__(user)
        self.builder = builder

    def generate(self):
        report = self.builder.set_transactions().build()
        template = TransactionReportTemplate(data=report)
        return template.export()
        # wb = Workbook()
        # ws = wb.active
        # ws.title = 'Transaction Report'
        #
        # headers = ['ID', 'Wallet', 'Category', 'Amount', 'Date']
        # ws.append(headers)
        #
        # for tx in self.builder.transactions:
        #     ws.append([
        #         tx.id,
        #         tx.wallet.name,
        #         tx.category.name,
        #         tx.amount,
        #         None
        #     ])
        #
        # response = HttpResponse(
        #     content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        # )
        # filename = f"transactions_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        # response["Content-Disposition"] = f"attachment; filename={filename}"
        # wb.save(response)
        # return response

