import pytest

from enums.wallet import WalletType
from wallet.models import Wallet


# ============================================ INIT DATA TEST =================================
# data test
@pytest.fixture()
def create_wallets(db):
    def do_create():
        return Wallet.objects.bulk_create([
            Wallet(balance=10000, name="WALLET_01", type=WalletType.CASH.name, user_id=1),
            Wallet(balance=20000, name="WALLET_02", type=WalletType.CASH.name, user_id=1),
            Wallet(balance=30000, name="WALLET_03", type=WalletType.BANK.name, user_id=1),
            Wallet(balance=10000, name="WALLET_04", type=WalletType.CASH.name, user_id=1),
        ])

    return do_create


# ============================================= HAPPY CASE =====================================

@pytest.mark.django_db
def test_create_wallet(client, login, user):
    auth = login(client, user)
    payload = {
        "name": 'Wallet_001',
        "balance": 10000,
        "type": "CASH"
    }
    response = auth('post', '/api/wallet/', payload)
    data = response.json()
    assert response.status_code == 201
    assert data['success'] == True
    assert data['data']['balance'] == payload['balance']
    assert data['data']['name'] == payload['name']
    assert data['data']['type'] == payload['type']


# ======================================================

@pytest.mark.django_db
def test_get_wallet(client, login, user, wallet_user_01):
    auth = login(client, user)
    response = auth('get', f'/api/wallet/{wallet_user_01.pk}')
    data = response.json()
    assert response.status_code == 200
    assert data['success'] == True
    assert data['data']['id'] == wallet_user_01.pk


# =======================================================

#  case params
get_params = [
    ({"type": "CASH"}, ['WALLET_01', 'WALLET_02', 'WALLET_04']),
    ({"user_id": 1}, ['WALLET_01', 'WALLET_02', 'WALLET_03', 'WALLET_04']),
    ({"user_id": 1, "type": WalletType.CASH.name}, ['WALLET_01', 'WALLET_02', 'WALLET_04']),
    ({"name": "WALLET_01", "type": WalletType.CASH.name}, ['WALLET_01']),
    ({"type": WalletType.BANK.name}, ['WALLET_03']),
    ({}, ['WALLET_01', 'WALLET_02', 'WALLET_03', 'WALLET_04']),
]


@pytest.mark.parametrize("get_param,expect_name", get_params)
def test_get_with_params(get_param, expect_name, client, login, user, create_wallets, ):
    create_wallets()
    auth = login(client, user)
    res = auth('get', f'/api/wallet/', data=get_param)
    data = res.json()
    returned_name = [item['name'] for item in data['data']]
    assert res.status_code == 200
    assert data['success'] == True
    assert sorted(returned_name) == sorted(expect_name)


# ==========================================================

@pytest.mark.django_db
def test_update_wallet(client, login, user, wallet_user_01):
    auth = login(client, user)
    payload = {
        "name": 'Wallet_001',
        "balance": '20000',
        "type": "CASH"
    }
    response = auth('put', f'/api/wallet/{wallet_user_01.pk}', payload)
    assert response.status_code == 200
    assert response.json()['success'] == True


# ===========================================================

@pytest.mark.django_db
def test_delete_wallet(client, login, user, wallet_user_01):
    auth = login(client, user)
    response = auth('delete', f'/api/wallet/{wallet_user_01.pk}')
    assert response.status_code == 200
    assert response.json()['success'] == True


# ============================================ UNEXPECT CASE ===================================

# Payload create validate failed
create_payloads = [
    {
        "balance": 'abc',
        "name": 'WALLET_01',
        "type": 'CASH',
    },
    {
        "balance": -10,
        "name": 'WALLET_02',
        "type": 'CASH',
    },
    {
        "name": 'WALLET_02',
        "type": 'CREDIT',
    },
    {
        "balance": 10000,
        "name": 'WALLET_02',
    },
    {
        "balance": 10000,
        "name": 'WALLET_02',
        "type": 'CREDIT',
        "invalid": 123
    },
]


@pytest.mark.parametrize("payload", create_payloads)
def test_create_validate_error_payload(client, login, user, payload, create_wallets):
    create_wallets()
    auth = login(client, user)
    res = auth('post', '/api/wallet/', payload)
    assert res.status_code == 422
    assert res.json()['success'] == False


# ============================================================

@pytest.mark.django_db
def test_wallet_name_unique(client, login, user, create_wallets):
    create_wallets()
    auth = login(client, user)
    payload = {
        "name": 'WALLET_02',
        "balance": 10000,
        "type": 'BANK'
    }
    res = auth('post', '/api/wallet/', data=payload)
    print('res', res.json())
    assert res.status_code == 422
