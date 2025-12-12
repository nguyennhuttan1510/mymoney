import json
from typing import Literal, List, Dict, Any
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction as transaction_db
from django.db.models import Sum, QuerySet
from pydantic.config import JsonEncoder

from budget.models import Budget
from budget.repository import BudgetRepository
from core.cache.key_generator import KeyHashing
from core.cache.redis import RedisCache, RedisSingleton
from core.exceptions.exceptions import BadRequest
from category.models import Category
from core.schema.service_abstract import ServiceAbstract
from transaction.models import Transaction
from transaction.repository import TransactionRepository
from transaction.schema import TransactionIn, TransactionUpdateSchema, TransactionQuery, TransactionListOut, \
    TransactionOut
from enums.transaction import TransactionType
from utils.cache import make_cache_key
from wallet.models import Wallet
from wallet.service import WalletService
from django.core.cache import cache


class Validator:
    @staticmethod
    def get_wallet(wallet_id: int) -> Wallet:
        try:
            return Wallet.objects.get(id=wallet_id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("Wallet does not exist.")

    @staticmethod
    def get_category(category_id: int) -> Category:
        try:
            return Category.objects.get(id=category_id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("Category does not exist.")

    @staticmethod
    def get_transaction(transaction_id: int, *args, ** kwargs) -> Transaction:
        try:
            return Transaction.objects.get(id=transaction_id, *args, ** kwargs)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("Transaction does not exist.")


class CachingTransaction(RedisCache):
    def __init__(self, prefix: str = "transactions_search"):
        super().__init__()
        self.prefix = prefix
        self.key = KeyHashing(prefix)

    def make_key(self, params):
        return self.key.generate(params)


class TransactionService(ServiceAbstract):
    repository = TransactionRepository()
    cache = CachingTransaction()

    @classmethod
    def destroy(cls, transaction_id: int, user:User) -> Transaction:
        transaction = Validator.get_transaction(transaction_id, user_id=user.pk)
        with transaction_db.atomic():
            WalletService.refund(wallet=transaction.wallet, category=transaction.category, amount=transaction.amount)
            cls.repository.delete(transaction_id)
        return transaction

    @classmethod
    def create(cls, payload: TransactionIn, user):
        wallet = Validator.get_wallet(wallet_id=payload.wallet)
        category = Validator.get_category(category_id=payload.category)

        with transaction_db.atomic():
            transaction = cls.repository.create({**payload.dict(by_alias=True), 'user_id': user.pk})
            WalletService.adjust(wallet, category, amount=payload.amount, transaction=transaction)
            return transaction

    @classmethod
    def update(cls, transaction_id: int, data:TransactionUpdateSchema, user: User) -> Transaction:
        transaction = Validator.get_transaction(transaction_id)
        wallet = Validator.get_wallet(wallet_id=data.wallet_id)
        category = Validator.get_category(category_id=data.category_id)

        with transaction_db.atomic():
            transaction_updated = cls.repository.update(instance=transaction, data={**data.dict(), 'user_id': user.pk})
            WalletService.refund(category=transaction.category, wallet=transaction.wallet, amount=transaction.amount)
            wallet.refresh_from_db(fields=['balance'])
            WalletService.adjust(category=category, wallet=wallet, amount=data.amount, transaction=transaction_updated)
            return transaction_updated

    @classmethod
    def search(cls, params: TransactionQuery) -> TransactionListOut:
        key = cls.cache.make_key(params.model_dump(exclude_none=True))
        def fetch():
            qs = cls.repository.get_all_for_user(params=params)
            return list(qs.values())
        data = cls.cache.get_or_set(key, ttl=360, fetch=fetch)

        # total = cls.repository.sum_amount(qs)
        return TransactionListOut(transactions=list(data), total=0)
