from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from core.exceptions.exceptions import BadRequest

from category.models import Category
from core.schema.response import CreateSuccessResponse
from transaction.models import Transaction as TransactionModel
from transaction.repository import TransactionRepository
from transaction.schema import TransactionCreateSchema
from utils.common import TransactionType
from django.db import transaction as transaction_db
from wallet.models import Wallet

class WalletProcessor:
    @staticmethod
    def adjust(wallet: Wallet, category: Category or TransactionType, amount: float):
        is_income = (category.type == TransactionType.INCOME if hasattr(category, 'type') else category == TransactionType.INCOME )
        delta = amount if is_income else -amount
        wallet.balance += delta
        wallet.save(update_fields=['balance'])

class Validator:
    @staticmethod
    def get_wallet(wallet_id: int) -> Wallet:
        try:
            return Wallet.objects.get(id=wallet_id)
        except ObjectDoesNotExist:
            raise BadRequest("Wallet does not exist.")

    @staticmethod
    def get_category(category_id: int) -> Category:
        try:
            return Category.objects.get(id=category_id)
        except ObjectDoesNotExist:
            raise BadRequest("Category does not exist.")

    @staticmethod
    def get_transaction(transaction_id: int) -> TransactionModel:
        try:
            return TransactionModel.objects.get(id=transaction_id)
        except ObjectDoesNotExist:
            raise BadRequest("Transaction does not exist.")


class TransactionService:
    transaction_repository = TransactionRepository()

    @classmethod
    def process(cls, payload: TransactionCreateSchema, user: User) -> TransactionModel:
        wallet = Validator.get_wallet(wallet_id=payload['wallet_id'])
        category = Validator.get_category(category_id=payload['category_id'])
        cls._ensure_positive_amount(amount=payload['amount'])
        cls._ensure_sufficient_balance(amount=payload['amount'], wallet=wallet, category=category)

        with transaction_db.atomic():
            WalletProcessor.adjust(wallet, category, amount=payload['amount'])
            transaction = cls.transaction_repository.create(**payload)
            return transaction

    def create_transaction(self, payload: TransactionCreateSchema, user):
        try:
            transaction = self.transaction_repository.create({**payload.dict(by_alias=True), 'user_id': user.pk})
        except Exception as e:
            raise BadRequest('Transaction create failed')

    @classmethod
    def destroy(cls, transaction_id: int) -> TransactionModel:
        transaction = Validator.get_transaction(transaction_id)
        reverse_type = (TransactionType.EXPENSE if transaction.category.type == TransactionType.INCOME else TransactionType.INCOME )
        transaction.category.type = reverse_type
        WalletProcessor.adjust(wallet=transaction.wallet, category=transaction.category, amount=transaction.amount)
        cls.transaction_repository.delete(transaction)
        return transaction

    @staticmethod
    def _ensure_positive_amount(amount: float) -> None:
        if amount <= 0:
            raise BadRequest("Amount must be positive.")

    @staticmethod
    def _ensure_sufficient_balance(
            amount: float, wallet: Wallet, category: Category
    ) -> None:
        if category.type == TransactionType.EXPENSE and wallet.balance < amount:
            raise BadRequest("Insufficient wallet balance.")
