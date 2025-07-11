import os.path
from abc import ABC, abstractmethod
from datetime import datetime

from django.http import HttpResponse
from openpyxl.reader.excel import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from typing_extensions import TypeVar, Generic, List

from report.patterns.builder import ReportBuilder, CategoryReportBuilder
from report.schema import ReportOut

T = TypeVar('T')

class ReportTemplateAbstract(Generic[T], ABC):
    def open_file_template(self, path: str):
        pass

    @abstractmethod
    def handle_data(self, file, data: [T]):
        pass

    @abstractmethod
    def initial_file(self, path_file: str):
        pass

    @abstractmethod
    def export(self):
        pass



class TransactionReportTemplate(ReportTemplateAbstract):
    def __init__(self, data: ReportOut):
        self.data = data

    def export(self):
        path = self.open_file_template('report-template.xlsx')
        wb = self.initial_file(path)
        ws = wb.active
        ws.title = 'Transaction Report'
        self.handle_data(ws, data=self.data)
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        filename = f"transactions_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        response["Content-Disposition"] = f"attachment; filename={filename}"
        wb.save(response)
        return response


    def open_file_template(self, file_name: str) -> str:
        return os.path.join('templates', file_name)

    def initial_file(self, path_file):
        # path_file = self.open_file_template('report-template.xlsx')
        wb = load_workbook(path_file)
        return wb

    def handle_data(self, ws: Worksheet, data: ReportOut):
        headers = ['ID', 'Wallet', 'Category', 'Amount', 'Date']
        ws.append(headers)

        for tx in data.transactions:
            ws.append([
                tx.id,
                tx.wallet.name,
                tx.category.name,
                tx.amount,
                None
            ])
        return ws




