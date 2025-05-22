from traceback import print_tb

import pytest
from transaction.models import Transaction


@pytest.mark.django_db
def test_create_transaction_unit(client, user_admin, login, wallet_admin_01):
    auth = login(client, user_admin)
    data = {
        "wallet_id": wallet_admin_01.pk,
        "amount": 10000,
        "category_id": 1,
        "transaction_date": "2025-04-25T08:32:21.775Z"
    }
    response = auth('post', '/api/transaction/', data)

    assert response.status_code == 200
    assert response.json()['data']["wallet"] == 1
    assert response.json()['data']["amount"] == "10000"
    assert Transaction.objects.count() == 1



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


@pytest.mark.parametrize('category_id, amount, category_id_edit, amount_edit, expected', [
    (3, 10000, 3, 20000, 30000),
    (3, 50000, 3, 10000, 40000),
    (3, 50000, 15, 10000, 60000),
])
def test_wallet_balance_after_edit_transaction(category_id, amount, category_id_edit, amount_edit, expected, client, user_admin, login, wallet_factory, admin_user):
    balance_provide = 50000
    auth = login(client, user_admin)

    wallet = wallet_factory(name='wallet_01', balance=balance_provide, user=admin_user)

    data = {
        "wallet_id": wallet.pk,
        "amount": amount,
        "category_id": category_id,
        "transaction_date": "2025-04-25T08:32:21.775Z"
    }
    response_transaction = auth('post', '/api/transaction/', data)

    transaction_id = response_transaction.json()['data']["id"]

# DATA UPDATE
    data = {
        **data,
        "amount": amount_edit,
        "category_id": category_id_edit
    }

    print('data', data)
    response = auth('put', f'/api/transaction/{transaction_id}', data)
    print('response', response.json()['data'])

    wallet.refresh_from_db()

    assert response.status_code == 200
    assert wallet.balance == expected


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

    assert response.status_code == 404




    assert "message" in response.json()
