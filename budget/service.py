from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound

from budget.models import Budget
from budget.repository import BudgetRepository
from budget.schema import BudgetIn
from core.schema.service_abstract import ServiceAbstract


class BudgetService(ServiceAbstract):
    repository = BudgetRepository()

    @classmethod
    def create_budget(cls, payload: BudgetIn):
        return cls.repository.create(payload.model_dump())

    @classmethod
    def get_all_budget_for_user(cls, user_id: int):
        return cls.repository.get_all_for_user(user_id=user_id)

    @classmethod
    def get_budget(cls, budget_id: int, user_id: int):
        try:
            return cls.repository.get_by_id(pk=budget_id, user_id=user_id)
        except ObjectDoesNotExist as e:
            ObjectDoesNotExist('budget not found')


    @classmethod
    def update_budget(cls, budget_id: int ,payload: BudgetIn, user_id:int):
        instance = cls.get_budget(budget_id=budget_id, user_id=user_id)
        return cls.repository.update(instance=instance, data=payload.model_dump())

    @classmethod
    def delete_budget(cls, budget_id: int, user_id: int):
        instance = cls.get_budget(budget_id=budget_id, user_id=user_id)
        return cls.repository.delete(instance.pk)