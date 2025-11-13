from abc import ABC, abstractmethod
from typing import TypeVar, Union, Type

from typing_extensions import Generic

from budget.models import Budget
from budget.schema import BudgetOut, BudgetOutCalculate
from transaction.schema import TransactionQuery
from transaction.service import TransactionService

T = TypeVar('T')


class BudgetBuilder(Generic[T]):
    def __init__(self, budget: Budget):
        self.budget = budget
        self._result: T = BudgetOut.from_orm(budget)

    def set_calculate(self):
        transactions = TransactionService.search(params=TransactionQuery(budget_id=self.budget.pk))
        self._result = BudgetOutCalculate(**self._result.model_dump(by_alias=True), total_spent=transactions.total, limit=self.budget.amount)
        return self

    def build(self) -> T:
        return self._result
