from typing import List, Optional
from utils.query import query_or_not
from wallet.models import Wallet


def create(data: dict) -> Wallet:
    return Wallet.objects.create(**data)

def get_all() -> List[Wallet]:
    return Wallet.objects.filter()

def get_by_id(wallet_id: int, *arg, **kwargs) -> Optional[Wallet]:
    return Wallet.objects.get(pk=wallet_id, *arg, **kwargs)

def update(wallet: Wallet, data: dict) -> Optional[Wallet]:
    for field, value in data.items():
        setattr(wallet, field, value)
    wallet.save()
    return wallet

def delete(wallet: Wallet):
    wallet.delete()
