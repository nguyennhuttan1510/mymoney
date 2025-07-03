import pytest

from budget.models import Budget
from budget.service import BudgetService
from enums.budget import BudgetStatus
from tests.helper import create_transaction, create_wallet, create_budget


@pytest.mark.django_db
@pytest.fixture()
def init_data_test(db, user):
    def init():
        wallet_01 = create_wallet('wallet_01', 100000, user)
        wallet_02 = create_wallet('wallet_02', 20000, user)

        create_transaction(wallet_id=wallet_01.pk, amount=5000, category_id=1, transaction_date='2025-06-23', user_id=user.pk)
        create_transaction(wallet_id=wallet_01.pk, amount=5000, category_id=1, transaction_date='2025-06-23', user_id=user.pk)
        create_transaction(wallet_id=wallet_01.pk, amount=5000, category_id=2, transaction_date='2025-06-23', user_id=user.pk)
        create_transaction(wallet_id=wallet_01.pk, amount=5000, category_id=3, transaction_date='2025-06-23', user_id=user.pk)
        create_transaction(wallet_id=wallet_02.pk, amount=4000, category_id=3, transaction_date='2025-06-23', user_id=user.pk)
        create_transaction(wallet_id=wallet_02.pk, amount=10000, category_id=2, transaction_date='2025-06-23', user_id=user.pk)
        create_transaction(wallet_id=wallet_02.pk, amount=15000, category_id=2, transaction_date='2025-06-23', user_id=user.pk)
        create_transaction(wallet_id=wallet_02.pk, amount=5000, category_id=1, transaction_date='2025-06-23', user_id=user.pk)

        budget_01 = create_budget(name='Category_1', amount=20000, start_date='2025-06-22', end_date='2025-06-26')
        budget_01.category.set([1])
        budget_01.wallet.set([1,2])
        budget_02 = create_budget(name='Category_2', amount=20000, start_date='2025-06-22', end_date='2025-06-26')
        budget_02.category.set([2])
        budget_02.wallet.set([2])
        budget_03 = create_budget(name='Category_3', amount=10000, start_date='2025-06-22', end_date='2025-06-26')
        budget_03.category.set([3])
        budget_03.wallet.set([1,2])
    return init


test_case = [
    (1, (15000, 75, BudgetStatus.OK.value)),
    (2, (25000, 125, BudgetStatus.OVER.value)),
    (3, (9000, 90, BudgetStatus.WARNING.value)),
]


@pytest.mark.django_db
@pytest.mark.parametrize('budget_input,expect', test_case)
def test_calculate_budget(init_data_test, budget_input, expect):
    init_data_test()
    (total_spent, usage_percent, status) = expect
    budget = Budget.objects.get(pk=budget_input)
    calc_schema = BudgetService.calculate_budget(budget=budget)
    assert float(calc_schema.total_spent) == float(total_spent)
    assert int(calc_schema.usage_percent) ==  usage_percent
    assert calc_schema.status == status
    assert float(calc_schema.limit) == float(budget.amount)
