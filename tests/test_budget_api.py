import pytest

from budget.models import Budget
from category.models import Category
from tests.helper import create_wallet


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
def valid_payload(wallet_01):
    return {"name": "Budget", "amount": 10000, "wallets": [wallet_01.pk], "categories": [1],
            "description": "this is description"}


@pytest.fixture
def init_budget(wallet_01, wallet_02, wallet_03):
    def creat():
        budget_01 = Budget.objects.create(
            amount=10000,
            name='BUDGET_01',
            start_date='2025-06-22',
            end_date='2025-06-22'
        )
        budget_01.category.set(Category.objects.all())
        budget_01.wallet.set([wallet_01, wallet_02])

        budget_02 = Budget.objects.create(
            amount=20000,
            name='BUDGET_02',
            start_date='2025-06-22',
            end_date='2025-06-22'
        )
        budget_02.category.set([Category.objects.get(pk=1)])
        budget_02.wallet.set([wallet_02])

        budget_03 = Budget.objects.create(
            amount=30000,
            name='BUDGET_03',
            start_date='2025-06-22',
            end_date='2025-06-22'
        )
        budget_03.category.set([Category.objects.get(pk=1)])
        budget_03.wallet.set([wallet_02])
        return [budget_01, budget_02, budget_03]
    return creat


get_params = [
    ({'amount': 10000}, 1),
    ({'categories': [1]}, 3),
    ({'categories': [2]}, 1),
    ({'wallets': [2]}, 3),
    ({}, 3)
]


# =============================================================================

@pytest.mark.django_db
def test_create_budget_success(client, login, user, valid_payload):
    auth = login(client, user)
    res = auth('post', '/api/budget/', data=valid_payload)
    print('res', res.json())
    assert res.status_code == 201
    data = res.json()
    print('data', data)
    assert "id" in data['data']
    assert data['data']['amount'] == valid_payload['amount']
    assert len(data['data']['categories']) == len(valid_payload['categories'])
    assert len(data['data']['wallets']) == len(valid_payload['wallets'])


@pytest.mark.django_db
@pytest.mark.parametrize('param, expected', get_params)
def test_get_budget_with_param(client, login, user, param, expected, init_budget):
    init_budget()
    auth = login(client, user)
    res = auth('get', '/api/budget/', data=param)
    print('res', res.json())
    assert res.status_code == 200
    data = res.json()['data']
    assert len(data) == expected


@pytest.mark.django_db
def test_get_budget(client, login, user, init_budget):
    init_budget()
    auth = login(client, user)
    budget_expected = Budget.objects.get(pk=1)
    res = auth('get', f'/api/budget/{budget_expected.pk}')
    assert res.status_code == 200
    data = res.json()['data']
    assert data['amount'] == budget_expected.amount
    assert data['description'] == budget_expected.description
    assert len(data['categories']) == len(budget_expected.category.all())
    assert len(data['wallets']) == len(budget_expected.wallet.all())


@pytest.mark.django_db
def test_update_budget(client, login, user, wallet_01, wallet_02, init_budget):
    init_budget()
    auth = login(client, user)
    payload = {"amount": 10000, "categories": [1,2,3], 'wallets': [wallet_01.pk, wallet_02.pk],"description": "this is description"}
    res = auth('patch', f'/api/budget/{1}', data=payload)
    print(res.json())
    assert res.status_code == 200
    data = res.json()['data']
    assert data['amount'] == payload['amount']
    assert len(data['categories']) == len(payload['categories'])
    assert len(data['wallets']) == len(payload['wallets'])
    assert data['description'] == payload['description']


@pytest.mark.django_db
def test_delete_budget(client, login, user, init_budget):
    init_budget()
    auth = login(client, user)
    payload = {
        'ids': [1,2]
    }
    res = auth('delete', f'/api/budget/ids', data=payload)
    print(res.json())
    assert res.status_code == 200
    assert Budget.objects.filter(pk__in=payload['ids']).exists() == False


# ============================================== UNEXPECTED CASE ===========================================

#
# @pytest.mark.django_db
# def test_not_get_budget_of_other_user(client, login, user_admin, wallet_01, init_budget):
#     auth = login(client, user_admin)
#     budget = Budget.objects.get(wallet__id=wallet_01.pk)
#     res = auth('get', f'/api/budget/{budget.pk}')
#     assert res.status_code == 404


# @pytest.mark.django_db
# def test_delete_budget_other_user(client, login, user_admin, wallet_01, init_budget):
#     auth = login(client, user_admin)
#     budget = Budget.objects.get(wallet__id=wallet_01.pk)
#     res = auth('delete', f'/api/budget/{budget.pk}')
#     print('res', res.json())
#     assert res.status_code == 404
