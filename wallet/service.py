from django.contrib.auth.models import User

from category.models import Category
from utils.common import TransactionType
from wallet.models import Wallet
from wallet.repository import WalletRepository
from wallet.schema import WalletIn


class WalletService:
    repository = WalletRepository()

    @staticmethod
    def adjust(wallet: Wallet, category: Category or TransactionType, amount: float):
        is_income = (category.type == TransactionType.INCOME.value if hasattr(category, 'type') else category == TransactionType.INCOME )
        delta = amount if is_income else -amount
        wallet.balance += delta
        wallet.save(update_fields=['balance'])

    @classmethod
    def refund(cls, wallet: Wallet, category: Category or TransactionType, amount: float):
        reverse_type = (TransactionType.EXPENSE if category.type == TransactionType.INCOME else TransactionType.INCOME )
        return cls.adjust(category=reverse_type, wallet=wallet, amount=amount)

    @classmethod
    def create_wallet(cls, data: WalletIn, user: User):
        data = data.dict()
        data['user_id'] = user.pk
        return cls.repository.create(data=data)


    # @classmethod
    # def destroy(cls, instance: Wallet):
    #     return cls.adjust(category=reverse_type, wallet=wallet, amount=amount)