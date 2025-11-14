import os

import pytest
from django.contrib.auth import get_user_model
from django.db import connection

from budget.models import Budget
from category.models import Category
from enums.transaction import TransactionType
from enums.wallet import WalletType
from tests.helper import generate_token
from wallet.models import Wallet
from wallet.schema import WalletIn

User = get_user_model()

@pytest.fixture
def login(request):
    # def access(client, user):
    #     return auth_client(client, user)
    return request

def get_request(client, user=None):
    def wrapper(method, path, data=None):

        print(f"[DEBUG] HTTP method: {method.upper()} - URL: {path}")
        config = {
            "path": path,
            "data":data,
            "content_type":"application/json",
        }
        if user:
            access_token = generate_token(user)
            config.__setitem__("HTTP_AUTHORIZATION", f"Bearer {access_token}")

        return getattr(client, method)(**config)
    return wrapper

# @pytest.fixture
# def authentication(user):
#     user = User.objects.get(pk=user.pk)
#     token = str(RefreshToken.for_user(user=user))
#     client = APIClient()
#     client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
#     return client
#
#
# @pytest.fixture
# def user_admin():
#     return create_user(is_superuser=True, is_staff=True)
#
#
# @pytest.fixture
# def user():
#     return create_user(username='admin', password='o0i9u8y7', is_superuser=False, is_staff=False)
#
#
# @pytest.fixture
# def staff():
#     return create_user(username='staff', password='o0i9u8y7', is_superuser=False, is_staff=True)
#
#
# @pytest.fixture
# def wallet_admin_01(admin_user):
#     return create_wallet(name='wallet_admin_01', balance=5000000, user=admin_user)
#
#
# @pytest.fixture
# def wallet_admin_02(admin_user):
#     return create_wallet(name='wallet_admin_02', balance=6000000, user=admin_user)
#
#
# @pytest.fixture
# def wallet_staff_01(staff):
#     return create_wallet(name='wallet_staff_01', balance=5000000, user=staff)
#
#
# @pytest.fixture
# def wallet_staff_02(staff):
#     return create_wallet(name='wallet_staff_02', balance=6000000, user=staff)
#
#
# @pytest.fixture
# def wallet_user_01(user):
#     return create_wallet(name='wallet_user_01', balance=5000000, user=user)
#
#
# @pytest.fixture
# def wallet_user_02(user):
#     return create_wallet(name='wallet_user_02', balance=6000000, user=user)
#
# # ======================================= INIT DATABASE =======================================
#
# CATEGORY
@pytest.fixture(autouse=True, scope='session')
def load_categories_from_sql(django_db_setup, django_db_blocker):
    sql_path = os.path.join(os.path.dirname(__file__), 'sql', 'category.sql')
    print('sql_path', sql_path)
    with open(sql_path, 'r', encoding="utf-8") as file:
        sql = file.read()

    statements = [s.strip() for s in sql.split(";") if s.strip()]

    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            for statement in statements:
                try:
                    cursor.execute(statement)
                except Exception as e:
                    print(f"[WARN] Skipped SQL statement: {statement[:50]}... → {e}")





# ====================================================================


@pytest.fixture
def user(db):
    return User.objects.create_user(username="usertest", password="123456")

@pytest.fixture
def wallet(db, user):
    return Wallet.objects.create(user=user, name="Main Wallet", balance=1000000, type=WalletType.CASH.value)

@pytest.fixture
def category(db):
    return Category.objects.create(name="Food", type=TransactionType.INCOME.value)

@pytest.fixture
def budget(db, user, wallet, category):
    return Budget.objects.create(user=user, name="Food", amount=1000000, wallet=wallet, category=category)