import pytest
from rest_framework_simplejwt.tokens import RefreshToken

from budget.models import Budget
from category.models import Category
from django.contrib.auth.models import User

from enums.transaction import TransactionType
from enums.wallet import WalletType
from transaction.models import Transaction
from wallet.models import Wallet

def create_wallet(name="Default Wallet", balance=0, user=None, type: WalletType = WalletType.CASH.value) -> Wallet:
    return Wallet.objects.create(user=user, name=name, balance=balance, type=type)

@pytest.fixture
def create_user(db):
    def _create_user(username, password, **extra_field):
        return User.objects.create_user(username=username, password=password, **extra_field)
    return _create_user


def create_category(name='Category_1', category_type="INCOME") -> Category:
    return Category.objects.create(name=name, type=category_type)

def create_budget(*args, **kwargs) -> Budget:
    return Budget.objects.create(*args, **kwargs)


def create_transaction(*args, **kwargs) -> Transaction:
    return Transaction.objects.create(*args, **kwargs)


def generate_token(user):
    refresh_token = RefreshToken.for_user(user=user)
    return refresh_token.access_token
