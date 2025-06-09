from abc import ABC, abstractmethod

from django.core.exceptions import ValidationError, ObjectDoesNotExist

from transaction.models import Transaction as TransactionModel
from transaction.schema import TransactionCreateSchema
from utils.common import TransactionType
from django.db import transaction as transaction_db
from transaction import repository
from wallet import repository as repository_wallet
from wallet.models import Wallet

# === Payment Method Processors (Strategy Pattern) ===

class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, wallet: Wallet, amount: float):
        pass

    @abstractmethod
    def refund(self, wallet: Wallet, amount: float):
        pass


class CardProcessor(PaymentProcessor):
    def process(self, wallet: Wallet, amount: float):
        wallet.balance -= amount

    def refund(self, wallet: Wallet, amount: float):
        wallet.balance += amount

class CashProcessor(CardProcessor):
    pass


# === Transaction Operations Strategies ===

class TransactionStrategy(ABC):
    @abstractmethod
    def execute(self, **kwargs) -> TransactionModel:
        pass


class CreateTransactionStrategy(TransactionStrategy):
    def __init__(self, processor_map: dict[str, PaymentProcessor]):
        self.processor_map = processor_map


    def execute(self, payment_method: str, data_transaction: TransactionCreateSchema, **kwargs) -> TransactionModel:
        if data_transaction.amount <= 0:
            raise ValidationError("Amount must be positive.")

        processor = self.processor_map.get(payment_method)
        if not processor:
            raise ValidationError(f"Unsupported payment method: {payment_method}")

        try:
            wallet = Wallet.objects.select_for_update().get(pk=data_transaction.wallet_id)
        except Wallet.DoesNotExist:
            raise ObjectDoesNotExist(f'Wallet {data_transaction.wallet_id} not found')

        with transaction_db.atomic():
            processor.process(wallet=wallet, amount=data_transaction.amount)
            wallet.save(update_fields=['balance'])

            # Record transaction
            transaction = repository.create(data_transaction.dict())
            return transaction


class CancelTransactionStrategy(TransactionStrategy):
    def __init__(self, processor_map: dict[str, PaymentProcessor]):
        self.processor_map = processor_map

    def execute(self, transaction_id: int) -> TransactionModel:
        try:
            transaction = Transaction.objects.select_related('wallet').select_for_update().get(pk=transaction_id)
        except Transaction.DoesNotExist:
            raise ObjectDoesNotExist(f"Transaction {transaction_id} not found.")

        processor = self.processor_map.get(transaction.method)
        if not processor:
            raise ValidationError(f"Unsupported payment method: {transaction.method}")

        with transaction_db.atomic():
            # Refund via processor
            processor.refund(transaction.wallet, transaction.amount)
            transaction.wallet.save(update_fields=['balance'])

        return transaction


# === Service & Factory ===
class TransactionService:
    # Map available payment processors
    _processor_map = {
        'cash': CashProcessor(),
        'card': CardProcessor(),
        # Add more processors (e-wallet, bank-transfer) here
    }

    _strategies = {
        'create': CreateTransactionStrategy(_processor_map),
        'cancel': CancelTransactionStrategy(_processor_map),
    }

    @classmethod
    def execute(cls, action: str, **kwargs) -> TransactionModel:
        strategy = cls._strategies.get(action)
        if not strategy:
            raise KeyError(f"Unsupported action: {action}")
        return strategy.execute(**kwargs)




class Transaction:
    transaction: TransactionModel

    @staticmethod
    def _update_wallet_balance(wallet: Wallet, amount: float):
        wallet.balance += amount
        wallet.save()

    def _reset_balance(self, old_transaction: TransactionModel):
        multiplier = 1 if old_transaction.category.type == TransactionType.EXPENSE.value else -1
        wallet = repository_wallet.get_by_id(old_transaction.wallet.pk)
        self._update_wallet_balance(wallet, multiplier * old_transaction.amount)

    def change_balance(self):
        multiplier = 1 if self.transaction.category.type == TransactionType.INCOME.value else -1
        wallet = repository_wallet.get_by_id(self.transaction.wallet.pk)
        self._update_wallet_balance(wallet, multiplier * self.transaction.amount)

    @abstractmethod
    def process(self) -> TransactionModel:
        pass

    def cancel(self):
        pass



class SpendingTransaction(Transaction):
    transaction = None

    def __init__(self, transaction: TransactionModel):
        self.transaction = transaction


    def process(self):
        try:
            with transaction_db.atomic():
                is_new = self.transaction.pk is None

                if is_new:
                    self.change_balance()
                else:
                    old_transaction = repository.get_by_id(self.transaction.pk)
                    if old_transaction.amount != self.transaction.amount or old_transaction.category.type != self.transaction.category.type or old_transaction.wallet != self.transaction.wallet:
                        self._reset_balance(old_transaction)
                        self.change_balance()

                self.transaction.save()
                return self.transaction
        except Exception as e:
            raise e


    def cancel(self):
        repository.delete(self.transaction)
        self._reset_balance(self.transaction)





