from http.client import HTTPException

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from ninja import PatchDict

from budget.models import Budget
from budget.repository import BudgetRepository
from budget.schema import BudgetIn, BudgetUpdate
from core.schema.service_abstract import ServiceAbstract
from django.db import transaction as transaction_db

from enums.wallet import WalletType
from wallet.repository import WalletRepository
from wallet.schema import WalletIn
from wallet.service import WalletService


class BudgetService(ServiceAbstract):
    repository = BudgetRepository()

    @classmethod
    def create_budget(cls, payload: BudgetIn):
        try:
            return cls.repository.create(payload.model_dump())
        except Exception as e:
            print('error', e)
            raise Exception(f'create budget failed - {e}')

    @classmethod
    def get_all_budget_for_user(cls, user_id: int, *args, **kwargs):
        return cls.repository.get_all_for_user(user_id=user_id, *args, **kwargs)

    @classmethod
    def get_budget(cls, budget_id: int, user_id: int) -> Budget:
        try:
            return cls.repository.get_by_id(pk=budget_id, wallet__user__pk=user_id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('budget not found')

    @classmethod
    def update_budget(cls, budget_id: int, payload: BudgetUpdate, user_id: int):
        instance = cls.get_budget(budget_id=budget_id, user_id=user_id)
        return cls.repository.update(instance=instance, data=payload.dict(exclude_unset=True))

    @classmethod
    def delete_budget(cls, budget_id: int, user_id: int):
        instance = cls.get_budget(budget_id=budget_id, user_id=user_id)
        with transaction_db.atomic():
            instance.wallet.delete()
            return cls.repository.delete(instance)
