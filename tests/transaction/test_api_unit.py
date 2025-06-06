from traceback import print_tb

import pytest

from category.models import Category
from transaction.models import Transaction
from wallet.models import Wallet

@pytest.fixture
def create_transaction(db):
    def make_transaction(**kwargs):
        return Transaction.objects.create(**kwargs)
    return make_transaction

@pytest.mark.django_db
def test_create_transaction_unit(client, user_admin, login, wallet_admin_01):
    auth = login(client, user_admin)
    data = {
        "wallet_id": wallet_admin_01.pk,
        "amount": 10000,
        "category_id": 1,
    }
    response = auth('post', '/api/transaction/', data)

    assert response.status_code == 200
    assert response.json()['data']["wallet"] == 1
    assert response.json()['data']["amount"] == 10000


@pytest.mark.django_db
def test_wallet_balance_after_transaction(client, user_admin, login, wallet_admin_01):
    auth = login(client, user_admin)

    wallet_admin_01.balance = 50000
    wallet_admin_01.save()

    data = {
        "wallet_id": wallet_admin_01.pk,
        "amount": 10000,
        "category_id": 1,
        "transaction_date": "2025-04-25T08:32:21.775Z"
    }
    response = auth('post', '/api/transaction/', data)

    wallet_admin_01.refresh_from_db()

    assert response.status_code == 200
    assert wallet_admin_01.balance == 40000


@pytest.mark.parametrize('wallet, category_id, amount, wallet_edit, category_id_edit, amount_edit, wallet_expected, wallet_2_expected', [
    ('wallet_admin_01', 3, 10000, 'wallet_admin_01', 3, 20000, 30000, 50000),
    ('wallet_admin_01', 3, 50000, 'wallet_admin_01', 3, 10000, 40000, 50000),
    ('wallet_admin_01',3, 50000, 'wallet_admin_01', 15, 10000, 60000, 50000),
    ('wallet_admin_01',3, 50000, 'wallet_admin_02', 15, 10000, 50000, 60000),
    ('wallet_admin_01',3, 2000, 'wallet_admin_02', 15, 30000, 50000, 80000),
])
def test_wallet_balance_after_edit_transaction(wallet, category_id, amount, wallet_edit, category_id_edit, amount_edit, wallet_expected, wallet_2_expected, client, user_admin, login, wallet_admin_01, wallet_admin_02):
    balance_provide = 50000
    wallet_admin_01.balance = balance_provide
    wallet_admin_02.balance = balance_provide

    wallet_admin_01.save()
    wallet_admin_02.save()

    auth = login(client, user_admin)

    wallet = Wallet.objects.get(name=wallet)
    wallet_2 = Wallet.objects.get(name=wallet_edit)

    print('wallet begin', wallet.balance)

    data = {
        "wallet_id": wallet.pk,
        "amount": amount,
        "category_id": category_id,
        "transaction_date": "2025-04-25T08:32:21.775Z"
    }
    response_transaction = auth('post', '/api/transaction/', data)

    wallet.refresh_from_db()

    print('wallet before', wallet.balance)

    transaction_id = response_transaction.json()['data']["id"]

# DATA UPDATE
    data = {
        "wallet_id": wallet_2.pk,
        "amount": amount_edit,
        "category_id": category_id_edit
    }

    print('data', data)
    response = auth('put', f'/api/transaction/{transaction_id}', data)
    print('response', response.json())
    print('response', response.json()['data'])

    wallet.refresh_from_db()
    wallet_2.refresh_from_db()

    print('wallet after', wallet.balance)

    assert response.status_code == 200
    assert wallet.balance == wallet_expected
    # assert wallet_2.balance == wallet_2_expected


@pytest.mark.django_db
def test_transaction_invalid_wallet_and_category(client, user_admin, login):
    auth = login(client, user_admin)
    instance_not_found = 999
    data = {
        "wallet_id": instance_not_found,
        "amount": 10000,
        "category_id": instance_not_found,
        "transaction_date": "2025-04-25T08:32:21.775Z"
    }
    response = auth('post', '/api/transaction/', data)
    print('response', response.json())

    assert response.status_code == 400


@pytest.mark.django_db
def test_transaction_removed(client, user, login, wallet_user_01, create_transaction):
    auth = login(client, user)
    data = {
        "wallet_id": wallet_user_01.pk,
        "amount": 10000,
        "category_id": 3,
        "user_id": user.pk
    }
    transaction = create_transaction(**data)
    response_delete = auth('delete', f'/api/transaction/{transaction.pk}', None)
    assert response_delete.status_code == 200
