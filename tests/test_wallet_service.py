import pytest

from category.models import Category
from enums.wallet import WalletType
from wallet.models import Wallet
from wallet.service import WalletService
#
@pytest.fixture
def init_data(user):
    def create_wallet():
        Wallet.objects.create(balance=100000, name="WALLET_01", type=WalletType.CASH.name, user_id=user.pk)
    return create_wallet

# ============================================

params = [
    (1, 5000, 95000),
    (2, 12300, 87700),
    (15, 20000, 120000),
]

@pytest.mark.django_db
@pytest.mark.parametrize('category,amount,expected', params)
def test_calculate_balance(init_data, category, amount, expected):
    init_data()
    wallet = Wallet.objects.get(name='WALLET_01')
    category_instance = Category.objects.get(pk=category)
    WalletService.adjust(wallet=wallet, category=category_instance, amount=amount)
    wallet.refresh_from_db()
    assert wallet.balance == expected