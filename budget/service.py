from http.client import HTTPException

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from ninja import PatchDict
from budget.repository import BudgetRepository
from budget.schema import BudgetIn, BudgetUpdate
from core.schema.service_abstract import ServiceAbstract


class BudgetService(ServiceAbstract):
    repository = BudgetRepository()

    @classmethod
    def create_budget(cls, payload: BudgetIn):
        cls._check_wallet_existed(wallet_id=payload.wallet)
        try:
            return cls.repository.create(payload.model_dump(by_alias=True))
        except Exception as e:
            print('error', e)
            raise Exception('create budget failed')

    @classmethod
    def get_all_budget_for_user(cls, user_id: int, *args, **kwargs):
        return cls.repository.get_all_for_user(user_id=user_id, *args, **kwargs)

    @classmethod
    def get_budget(cls, budget_id: int, user_id: int):
        try:
            return cls.repository.get_by_id(pk=budget_id)
        except ObjectDoesNotExist:
            ObjectDoesNotExist('budget not found')

    @classmethod
    def update_budget(cls, budget_id: int ,payload: BudgetUpdate, user_id:int):
        instance = cls.get_budget(budget_id=budget_id, user_id=user_id)
        return cls.repository.update(instance=instance, data=payload.dict(exclude_unset=True))

    @classmethod
    def delete_budget(cls, budget_id: int, user_id: int):
        instance = cls.get_budget(budget_id=budget_id, user_id=user_id)
        return cls.repository.delete(instance)

    @classmethod
    def _check_wallet_existed(cls, wallet_id: int):
        wallet_existed = cls.repository.filter(wallet_id=wallet_id).exists()
        if wallet_existed:
            raise ValueError(f'Wallet {wallet_id} have existed in other budget')
        # pass