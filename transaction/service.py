from typing import Literal
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction as transaction_db

from core.exceptions.exceptions import BadRequest
from category.models import Category
from core.schema.service_abstract import ServiceAbstract
from transaction.models import Transaction
from transaction.repository import TransactionRepository
from transaction.schema import TransactionIn, TransactionUpdateSchema
from enums.transaction import TransactionType
from wallet.models import Wallet
from wallet.service import WalletService


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
            cls.repository.delete(transaction)
        return transaction

    @classmethod
    def _create_transaction(cls, payload: TransactionIn, user):
        wallet = Validator.get_wallet(wallet_id=payload.wallet)
        category = Validator.get_category(category_id=payload.category)
        cls._ensure_positive_amount(amount=payload.amount)
        cls._ensure_sufficient_balance(amount=payload.amount, wallet=wallet, category=category)

        with transaction_db.atomic():
            WalletService.adjust(wallet, category, amount=payload.amount)
            transaction = cls.repository.create({**payload.dict(by_alias=True), 'user_id': user.pk})
            return transaction

    @classmethod
    def _update_transaction(cls, transaction_id: int, data:TransactionUpdateSchema, user: User) -> Transaction:
        transaction = Validator.get_transaction(transaction_id)
        wallet = Validator.get_wallet(wallet_id=data.wallet_id)
        category = Validator.get_category(category_id=data.category_id)
        cls._ensure_positive_amount(amount=data.amount)
        cls._ensure_sufficient_balance(amount=data.amount, wallet=wallet, category=category)

        with transaction_db.atomic():
            WalletService.refund(category=transaction.category, wallet=transaction.wallet, amount=transaction.amount)
            wallet.refresh_from_db(fields=['balance'])
            WalletService.adjust(category=category, wallet=wallet, amount=data.amount)
            transaction_updated = cls.repository.update(instance=transaction, data={**data.dict(), 'user_id': user.pk})
            return transaction_updated

    @staticmethod
    def _ensure_positive_amount(amount: float) -> None:
        if amount <= 0:
            raise BadRequest("Amount must be positive.")

    @staticmethod
    def _ensure_sufficient_balance(amount: float, wallet: Wallet, category: Category) -> None:
        if category.type == TransactionType.EXPENSE and wallet.balance < amount:
            raise BadRequest("Insufficient wallet balance.")
