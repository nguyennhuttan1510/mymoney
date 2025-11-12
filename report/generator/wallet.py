from report.patterns.builder import ReportBuilder
from report.patterns.report_strategy import BaseReportStrategy

from report.patterns.report_template_method import TransactionReportTemplate
from report.schema import ReportOut


class TransactionReportGenerator(BaseReportStrategy):
    def __init__(self, builder: ReportBuilder[ReportOut], user):
        super().__init__(user)
        self.builder = builder

    def generate(self):
        report = self.builder.set_category().set_wallet().set_transactions().build()
        template = TransactionReportTemplate(data=report)
        return template.export()
