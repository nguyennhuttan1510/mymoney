from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, BadRequest
from ninja import PatchDict, Query
from category.models import Category
from core.schema.service_abstract import ServiceAbstract
from enums.transaction import TransactionType
from transaction.models import Transaction
from wallet.models import Wallet
from wallet.repository import WalletRepository
from wallet.schema import WalletIn, WalletParam


class WalletService(ServiceAbstract):
    repository = WalletRepository()

    @staticmethod
    def adjust(wallet: Wallet, category: Category or TransactionType, amount: float, transaction: Transaction):
        is_income = (category.type == TransactionType.INCOME.value if hasattr(category,
                                                                              'type') else category == TransactionType.INCOME)
        delta = amount if is_income else -amount
        wallet.balance += delta
        transaction.balance = wallet.balance
        transaction.save(update_fields=['balance'])
        wallet.save(update_fields=['balance'])

    @classmethod
    def refund(cls, wallet: Wallet, category: Category or TransactionType, amount: float):
        reverse_type = (TransactionType.EXPENSE if category.type == TransactionType.INCOME else TransactionType.INCOME)
        return cls.adjust(category=reverse_type, wallet=wallet, amount=amount)

    @classmethod
    def create_wallet(cls, data: WalletIn, user: User):
        cls._validate_unique_name_wallet(wallet_name=data.name, user_id=user.pk)
        data = data.model_dump()
        data['user_id'] = user.pk
        return cls.repository.create(data=data)

    @classmethod
    def destroy(cls, wallet_id: int, user: User):
        instance = cls.get_wallet_by_id(wallet_id=wallet_id, user=user)
        return instance.delete()

    @classmethod
    def get_wallet_by_id(cls, wallet_id: int, user: User):
        try:
            return cls.repository.get_by_id(pk=wallet_id, user_id=user.pk)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("Wallet does not exist.")

    @classmethod
    def update(cls, wallet_id: int, data: PatchDict[WalletIn], user: User):
        instance = cls.get_wallet_by_id(wallet_id=wallet_id, user=user)
        return cls.repository.update(instance=instance, data=data)

    @classmethod
    def search(cls, query: Query[WalletParam]):
        return cls.repository.search(query)

    @classmethod
    def _validate_unique_name_wallet(cls, *args, **kwargs):
        exist = cls.repository.check_existed(*args, **kwargs)
        if exist:
            raise ValueError('wallet name existed')
