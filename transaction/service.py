import json
from typing import Literal, List
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction as transaction_db
from django.db.models import Sum, QuerySet
from pydantic.config import JsonEncoder

from budget.models import Budget
from budget.repository import BudgetRepository
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


class TransactionService(ServiceAbstract):
    repository = TransactionRepository()

    @classmethod
    def process(cls, payload: TransactionIn | TransactionUpdateSchema, user: User, action: Literal['create' , 'update'], transaction_id: int = None) -> Transaction:
        if action == 'create':
            return cls._create_transaction(payload=payload, user=user)
        else:
            return cls._update_transaction(transaction_id=transaction_id, user=user, data=payload)

    @classmethod
    def destroy(cls, transaction_id: int, user:User) -> Transaction:
        transaction = Validator.get_transaction(transaction_id, user_id=user.pk)
        with transaction_db.atomic():
            WalletService.refund(wallet=transaction.wallet, category=transaction.category, amount=transaction.amount)
            cls.repository.delete(transaction_id)
        return transaction

    @classmethod
    def _create_transaction(cls, payload: TransactionIn, user):
        wallet = Validator.get_wallet(wallet_id=payload.wallet)
        category = Validator.get_category(category_id=payload.category)

        with transaction_db.atomic():
            transaction = cls.repository.create({**payload.dict(by_alias=True), 'user_id': user.pk})
            WalletService.adjust(wallet, category, amount=payload.amount, transaction=transaction)
            return transaction

    @classmethod
    def _update_transaction(cls, transaction_id: int, data:TransactionUpdateSchema, user: User) -> Transaction:
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

        key = make_cache_key("transactions_search", params.model_dump(exclude_none=True))
        cached = cache.get(key)
        if cached:
            return TransactionListOut(transactions=list(json.loads(cached)), total=0)

        qs = cls.repository.get_all_for_user(params=params)
        # total = cls.repository.sum_amount(qs)

        cache.set(key, json.dumps(list(qs.values()), cls=DjangoJSONEncoder), timeout=360)

        return TransactionListOut(transactions=list(qs), total=0)
