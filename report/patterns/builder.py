from abc import ABC, abstractmethod
from ninja import Query
from typing_extensions import Generic, TypeVar

from category.models import Category
from report.schema import ReportOut, WalletReport
from tests.test_wallet_service import params
from transaction.repository import TransactionRepository
from transaction.schema import TransactionQueryParams
from transaction.service import TransactionService

T = TypeVar('T')

class ReportBuilder(Generic[T], ABC):
    # def __init__(self, data: list[T]):
    #     self.result: T = None
    #     self.data = data

    @abstractmethod
    def set_transactions(self) -> 'ReportBuilder[T]':
        pass

    @abstractmethod
    def set_wallet(self) -> 'ReportBuilder[T]':
        pass

    @abstractmethod
    def set_category(self) -> 'ReportBuilder[T]':
        pass

    @abstractmethod
    def calculate_total(self) -> 'ReportBuilder[T]':
        pass

    def build(self) -> T:
        pass


class CategoryReportBuilder(ReportBuilder[ReportOut]):
    repository = TransactionRepository()
    def __init__(self, params: Query[TransactionQueryParams]):
        self.params = params
        self.qs = self.repository.get_all_for_user(params=params)
        self._result: ReportOut = ReportOut(start_date=params.start_date, end_date=params.end_date)
        self._set_field_base()

    def _set_field_base(self):
        self._result.total = self.repository.sum_amount(self.qs)
        self._result.count_transaction = self.qs.count()

    def set_transactions(self):
        self._result.transactions = self.qs
        return self

    def set_wallet(self):
        self._result.wallets = [
            WalletReport.model_validate(obj={**obj, 'percent':self._calculate_percent(self._result.total, obj['total'])})
            for obj in self.repository.group_by(self.qs, 'wallet')
        ]
        return self

    def set_category(self):
        self._result.categories = [
            WalletReport.model_validate(obj={**obj, 'percent':self._calculate_percent(self._result.total, obj['total'])})
            for obj in self.repository.group_by(self.qs, 'category')
        ]
        return self

    def calculate_total(self):
        return self

    @staticmethod
    def _calculate_percent(total, part):
        return round((float(part)/float(total)) * 100, 2)

    def build(self):
        return self._result