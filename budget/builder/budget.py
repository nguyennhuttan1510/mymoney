from abc import ABC, abstractmethod
from typing import TypeVar, Union, Type

from typing_extensions import Generic

from budget.models import Budget
from budget.schema import BudgetOut, BudgetOutCalculate
from transaction.repository import TransactionRepository
from transaction.schema import TransactionQueryParams
from transaction.service import TransactionService

T = TypeVar('T')

class BudgetBuilder:
    def __init__(self, budget: Budget):
        self.budget = budget
        self._result: Union[Type[BudgetOut, BudgetOutCalculate]] = BudgetOut.model_validate(obj=budget)


    def set_calculate(self):
        response = TransactionService.search(params=TransactionQueryParams(budget=self.budget.pk))
        self._result = BudgetOutCalculate(total_spent=response.total, limit=self.budget.amount, **self._result.dict())
        return self


    def build(self) -> T:
        pass
