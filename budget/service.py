from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction as transaction_db
from django.db.models import Sum

from budget.models import Budget
from budget.repository import BudgetRepository
from budget.schema import BudgetIn, BudgetUpdate, BudgetOutWithCategory
from core.schema.service_abstract import ServiceAbstract
from enums.budget import BudgetStatus
from transaction.service import TransactionService


class BudgetService(ServiceAbstract):
    repository = BudgetRepository()

    @classmethod
    def create_budget(cls, payload: BudgetIn):
        try:
            instance = cls.repository.create(payload.model_dump())
            return instance
        except Exception as e:
            print('error', e)
            raise Exception(f'create budget failed - {e}')

    @classmethod
    def get_all_budget_for_user(cls, user_id: int, params):
        return cls.repository.get_all_for_user(user_id=user_id, params=params)

    @classmethod
    def get_budget_with_category(cls, budget_id: int) -> BudgetOutWithCategory | None:
        instance = cls.get_budget(budget_id=budget_id)
        calculate = cls.calculate_budget(instance)
        schema = BudgetOutWithCategory.model_validate(instance)
        schema.status = calculate.get('status')
        schema.total_spent = calculate.get('total_spent')
        schema.limit = calculate.get('limit')
        schema.usage_percent = calculate.get('usage_percent')
        return schema

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
    def delete_budget(cls, budget_id: int, user_id: int):
        instance = cls.get_budget(budget_id=budget_id)
        with transaction_db.atomic():
            return cls.repository.delete(instance)

    @classmethod
    def calculate_budget(cls, budget: Budget) -> dict:
        transactions = TransactionService.repository.filter(wallet__in=budget.wallet.all(), category__in=budget.category.all(), transaction_date__range=(budget.start_date, budget.end_date))
        total_spent = transactions.aggregate(total=Sum('amount'))['total'] or 0
        usage_percent = (total_spent/budget.amount) * 100

        if usage_percent > 100:
            status = BudgetStatus.OVER
        elif usage_percent >= 80:
            status = BudgetStatus.WARNING
        else:
            status = BudgetStatus.OK

        return {
            'total_spent': total_spent,
            'limit': budget.amount,
            'usage_percent': usage_percent,
            'status': status
        }
