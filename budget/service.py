from typing import Any, List

from django.core.exceptions import ObjectDoesNotExist

from budget.models import Budget
from budget.repository import BudgetRepository, BudgetDeleteSpecification
from budget.schema import BudgetIn, BudgetUpdate, BudgetOut, CalculatorBudget, BudgetDeleteIn
from core.schema.service_abstract import ServiceAbstract
from transaction.schema import TransactionQueryParams
from transaction.service import TransactionService


class BudgetService(ServiceAbstract):
    repository = BudgetRepository()

    @classmethod
    def create_budget(cls, payload: BudgetIn):
        try:
            instance = cls.repository.create(payload.model_dump(exclude_none=True))
            return instance
        except Exception as e:
            print('error', e)
            raise Exception(f'create budget failed - {e}')

    @classmethod
    def get_all_budget_for_user(cls, user_id: int, params):
        return cls.repository.get_all_for_user(user_id=user_id, params=params)

    @classmethod
    def get_budget_with_calculate(cls, instance: Budget) -> dict[Any, Any]:
        calc = cls.calculate_budget(instance)
        schema = BudgetOut.model_validate(instance).model_dump(by_alias=True)
        return {**schema, **calc.model_dump()}

    @classmethod
    def get_budget(cls, budget_id: int):
        try:
            return cls.repository.get_by_id(pk=budget_id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('budget not found')

    @classmethod
    def update_budget(cls, budget_id: int, payload: BudgetUpdate, user_id: int):
        update_data = payload.dict(exclude_unset=True)
        instance = cls.get_budget(budget_id=budget_id)
        return cls.repository.update(instance=instance, data=update_data)

    @classmethod
    def delete_budget(cls, payload: BudgetDeleteIn, user_id: int):
        specification = BudgetDeleteSpecification(params=payload)
        qs = cls.repository.filter(specification)
        return cls.repository.delete(qs)

    @classmethod
    def calculate_budget(cls, budget: Budget) -> CalculatorBudget:
        result = TransactionService.search(params=TransactionQueryParams(by_budget_id=budget.pk))
        return CalculatorBudget(total_spent=result.total, limit=budget.amount)
