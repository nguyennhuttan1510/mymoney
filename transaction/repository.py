from typing import List, Optional

from django.contrib.auth.models import User

from transaction.models import Transaction


def create(data: dict) -> Transaction:
    return Transaction.objects.create(**data)

def get_all(user: User, *args, **kwarg) -> List[Transaction]:
    return Transaction.objects.filter(user=user, *args, **kwarg)

def get_by_id(transaction_id: int) -> Optional[Transaction]:
    return Transaction.objects.get(pk=transaction_id)

def update(transaction: Transaction, data: dict) -> Optional[Transaction]:
    for field, value in data.items():
        setattr(transaction, field, value)
    transaction.save()
    return transaction

def delete(transaction: Transaction):
    transaction.delete()
