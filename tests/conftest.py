from tokenize import generate_tokens

import pytest
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from category.models import Category
from mymoney.api import api
from ninja.testing import TestClient

from tests.helper import auth_client
from wallet.models import Wallet

# FACTORY

@pytest.fixture
def user_factory(db):
    def user_create(username="admin", password="o0i9u8y7", **extra_field):
        return User.objects.create_user(username=username, password=password, **extra_field)
    return user_create

@pytest.fixture
def access_token_factory(user_admin):
    def generate_token(user=user_admin):
        refresh_token = RefreshToken.for_user(user=user)
        return refresh_token.access_token
    return generate_token

@pytest.fixture
def wallet_factory(user_admin):
    def create_wallet(name="Default Wallet", balance=0, user=user_admin) -> Wallet:
        return Wallet.objects.create(user=user, name=name, balance=balance)
    return create_wallet

@pytest.fixture
def category_factory():
    def create_category(name='Category_1', category_type="INCOME") -> Wallet:
        return Category.objects.create(name=name, type=category_type)
    return create_category

@pytest.fixture
def login(access_token_factory):
    def access(client, user):
        access_token = access_token_factory(user)
        return auth_client(client, access_token)
    return access

# ======================================= INIT DATABASE =======================================

# CATEGORY
@pytest.fixture(scope='module')
def default_categories():
    return Category.objects.bulk_create([
        Category(name='Fee', category_type='EXPENSE'),
        Category(name='Bill', category_type='EXPENSE'),
        Category(name='Gas', category_type='EXPENSE'),
    ])


# USER
@pytest.fixture
def user_admin(user_factory):
    return user_factory(is_superuser=True, is_staff=True)

@pytest.fixture
def user(user_factory):
    return user_factory(username='client', password='o0i9u8y7' ,is_superuser=False, is_staff=False)

@pytest.fixture
def staff(user_factory):
    return user_factory(username='staff', password='o0i9u8y7' ,is_superuser=False, is_staff=True)


#WALLET
@pytest.fixture
def wallet_admin_01(wallet_factory, admin_user):
    return wallet_factory(name='wallet_admin_01', balance=5000000, user=admin_user)

@pytest.fixture
def wallet_admin_02(wallet_factory, admin_user):
    return wallet_factory(name='wallet_admin_02', balance=6000000, user=admin_user)

@pytest.fixture
def wallet_staff_01(wallet_factory, staff):
    return wallet_factory(name='wallet_staff_01', balance=5000000, user=staff)

@pytest.fixture
def wallet_staff_02(wallet_factory, staff):
    return wallet_factory(name='wallet_staff_02', balance=6000000, user=staff)

@pytest.fixture
def wallet_user_01(wallet_factory, user):
    return wallet_factory(name='wallet_user_01', balance=5000000, user=user)

@pytest.fixture
def wallet_user_02(wallet_factory, user):
    return wallet_factory(name='wallet_user_02', balance=6000000, user=user)

