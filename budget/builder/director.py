from typing import Union, Type

from budget.builder.budget import BudgetBuilder
from budget.schema import BudgetOut, BudgetOutCalculate, BudgetParam


class Director:
    def __init__(self, builder: BudgetBuilder[Union[Type[BudgetOut], Type[BudgetOutCalculate]]],
                 options: BudgetParam = BudgetParam()):
        self._builder = builder
        self._options = options

    def construct_budget_analyze(self):
        self._builder.set_calculate()

    def make(self):
        if self._options.is_calc:
            self.construct_budget_analyze()

        return self._builder.build()
