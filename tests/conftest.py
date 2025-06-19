from rest_framework.test import APIClient

import pytest
from django.contrib.auth.models import User
from django.db import connection
from rest_framework_simplejwt.tokens import RefreshToken

from tests.helper import create_user, create_wallet, auth_client
import os

@pytest.fixture
def login():
    def access(client, user):
        return auth_client(client, user)
    return access

@pytest.fixture
def authentication(user):
    user = User.objects.get(pk=user.pk)
    token = str(RefreshToken.for_user(user=user))
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def user_admin():
    return create_user(is_superuser=True, is_staff=True)


@pytest.fixture
def user():
    return create_user(username='client', password='o0i9u8y7', is_superuser=False, is_staff=False)


@pytest.fixture
def staff():
    return create_user(username='staff', password='o0i9u8y7', is_superuser=False, is_staff=True)


@pytest.fixture
def wallet_admin_01(admin_user):
    return create_wallet(name='wallet_admin_01', balance=5000000, user=admin_user)


@pytest.fixture
def wallet_admin_02(admin_user):
    return create_wallet(name='wallet_admin_02', balance=6000000, user=admin_user)


@pytest.fixture
def wallet_staff_01(staff):
    return create_wallet(name='wallet_staff_01', balance=5000000, user=staff)


@pytest.fixture
def wallet_staff_02(staff):
    return create_wallet(name='wallet_staff_02', balance=6000000, user=staff)


@pytest.fixture
def wallet_user_01(user):
    return create_wallet(name='wallet_user_01', balance=5000000, user=user)


@pytest.fixture
def wallet_user_02(user):
    return create_wallet(name='wallet_user_02', balance=6000000, user=user)

# ======================================= INIT DATABASE =======================================

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





