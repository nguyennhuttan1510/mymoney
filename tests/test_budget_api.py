import pytest

from budget.models import Budget
from enums.transaction import TransactionType
from tests.helper import create_wallet, create_category, create_budget
from wallet.models import Wallet


@pytest.fixture
def wallet_01(user):
    return create_wallet(name='wallet_user_01', balance=5000000, user=user)


@pytest.fixture
def wallet_02(user):
    return create_wallet(name='wallet_user_02', balance=5000000, user=user)


@pytest.fixture
def wallet_03(user):
    return create_wallet(name='wallet_user_02', balance=10000, user=user)


@pytest.fixture
def category_01():
    return create_category(name='Thuế', category_type=TransactionType.EXPENSE.value)


@pytest.fixture
def category_02():
    return create_category(name='Tín dụng', category_type=TransactionType.EXPENSE.value)


@pytest.fixture
def valid_payload(wallet_01, category_01):
    return {"amount": 10000, "wallet": {
        "name": "Wallet_010",
        "balance": 1000,
        "type": "CASH"
    }, "category_id": category_01.pk,
            "description": "this is description"}


@pytest.fixture
def init_budget(wallet_01, wallet_02, wallet_03):
    create_budget(amount=10000, category_id=1, wallet_id=wallet_01.pk)
    create_budget(amount=20000, category_id=1, wallet_id=wallet_02.pk)
    create_budget(amount=30000, category_id=2, wallet_id=wallet_03.pk)


get_params = [
    ({'amount': 10000}, 1),
    ({'category_id': 1}, 2),
    ({'category_id': 2}, 1),
    ({'wallet_id': 2}, 1),
    ({}, 3)
]


# =============================================================================

@pytest.mark.django_db
def test_create_budget_success(client, login, user, valid_payload):
    auth = login(client, user)
    res = auth('post', '/api/budget/', data=valid_payload)
    assert res.status_code == 201
    data = res.json()
    print('data', data)
    assert "id" in data['data']
    assert data['data']['amount'] == valid_payload['amount']
    assert data['data']['category']['id'] == valid_payload['category_id']
    assert data['data']['wallet']['name'] == valid_payload['wallet']['name']


@pytest.mark.django_db
@pytest.mark.parametrize('param, expected', get_params)
def test_get_budget_with_param(client, login, user, param, expected, init_budget):
    auth = login(client, user)
    res = auth('get', '/api/budget/', data=param)
    assert res.status_code == 200
    data = res.json()['data']
    assert len(data) == expected


@pytest.mark.django_db
def test_get_budget(client, login, user, wallet_01, init_budget):
    auth = login(client, user)
    budget_expected = Budget.objects.get(wallet_id=wallet_01.pk)

    print('budget_expected', budget_expected.__dict__)
    res = auth('get', f'/api/budget/{wallet_01.pk}')
    assert res.status_code == 200
    data = res.json()['data']
    assert data['amount'] == budget_expected.amount
    assert data['description'] == budget_expected.description
    assert data['category']['id'] == budget_expected.category.pk
    assert data['wallet']['id'] == wallet_01.pk


@pytest.mark.django_db
def test_update_budget(client, login, user, wallet_01, init_budget):
    auth = login(client, user)
    payload = {"amount": 10000, "category_id": 1, "description": "this is description"}
    budget = Budget.objects.get(wallet__id=wallet_01.pk)
    res = auth('patch', f'/api/budget/{budget.pk}', data=payload)
    print(res.json())
    assert res.status_code == 200
    data = res.json()['data']
    assert data['amount'] == payload['amount']
    assert data['category']['id'] == payload['category_id']
    assert data['description'] == payload['description']


@pytest.mark.django_db
def test_delete_budget(client, login, user, init_budget):
    auth = login(client, user)
    budgets = Budget.objects.all()
    budget_id = budgets[0].pk
    res = auth('delete', f'/api/budget/{budget_id}')
    print(res.json())
    assert res.status_code == 200
    assert Budget.objects.filter(pk=budget_id).exists() == False


@pytest.mark.django_db
def test_delete_budget_cascade_wallet(client, login, user, init_budget):
    auth = login(client, user)
    budgets = Budget.objects.all()
    budget_delete = budgets[0]
    res = auth('delete', f'/api/budget/{budget_delete.pk}')
    print(res.json())
    assert res.status_code == 200
    assert Budget.objects.filter(pk=budget_delete.pk).exists() == False


# ============================================== UNEXPECTED CASE ===========================================


@pytest.mark.django_db
def test_not_get_budget_of_other_user(client, login, user_admin, wallet_01, init_budget):
    auth = login(client, user_admin)
    budget = Budget.objects.get(wallet__id=wallet_01.pk)
    res = auth('get', f'/api/budget/{budget.pk}')
    assert res.status_code == 404


@pytest.mark.django_db
def test_delete_budget_other_user(client, login, user_admin, wallet_01, init_budget):
    auth = login(client, user_admin)
    budget = Budget.objects.get(wallet__id=wallet_01.pk)
    res = auth('delete', f'/api/budget/{budget.pk}')
    print('res', res.json())
    assert res.status_code == 404
