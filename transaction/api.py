from typing import List

from django.db import transaction as transaction_db
from django.shortcuts import get_object_or_404
from ninja import Router, NinjaAPI
from ninja import PatchDict
from rest_framework.exceptions import NotFound

from category.models import Category
from core.schema.response import ResponseSchema, Response
from services.auth_jwt import JWTAuth
from transaction.models import Transaction
from transaction.schema import TransactionSchema, TransactionCreateSchema
from wallet.models import Wallet

router = Router(tags=['Transaction'], auth=JWTAuth())

@router.post("/", response=ResponseSchema[TransactionSchema])
def create_transaction(request, payload: TransactionCreateSchema ) -> ResponseSchema[TransactionSchema]:
    try:
        with transaction_db.atomic():
            user = getattr(request, 'auth', None)
            category = Category.objects.get(pk=payload.category)
            wallet = Wallet.objects.get(pk=payload.wallet, user=user)
            transaction_data = {**payload.dict(), "category": category, "wallet": wallet}
            transaction = Transaction.objects.create(user=user ,**transaction_data)
            return Response(data=transaction, message='Created transaction successfully' )
    except Category.DoesNotExist:
        raise NotFound(f"Category with id {payload.category} does not exist")
    except Wallet.DoesNotExist:
        raise NotFound(f"Wallet with id {payload.wallet} does not exist")
    except Exception as e:
        raise Exception(e)


@router.get("/", response=ResponseSchema[List[TransactionSchema]])
def get_all_transaction(request):
    transactions = Transaction.objects.filter(user=request.user)
    return Response(data=transactions, message=f"Get all transactions of user {request.user.pk} successfully" )


@router.get("/{int:transaction_id}", response=ResponseSchema[TransactionSchema])
def get_transaction(request, transaction_id: int):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return Response(data=transaction, message=f"Get transactions {transaction.pk} successfully" )


@router.put("/{int:transaction_id}", response=ResponseSchema[TransactionSchema])
def update_transaction(request, transaction_id: int, item: PatchDict[TransactionCreateSchema]):
    try:
        transaction = get_object_or_404(Transaction, id=transaction_id)
        for key, value in item.items():
            if value is not None:
                if key == 'category':
                    category = Category.objects.get(pk=value)
                    value = category
                if key == 'wallet':
                    wallet = Wallet.objects.get(pk=value)
                    value = wallet
                setattr(transaction, key, value)

        transaction.save()
        return Response(data=transaction, message=f"Updated transactions {transaction.pk} of user {request.user.pk} successfully" )

    except Transaction.DoesNotExist:
        return Response(message=f"Transaction with id {id} does not exist" )


@router.delete("/{int:transaction_id}", response=ResponseSchema)
def delete_transaction(request, transaction_id: int):
    try:
        transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        transaction.delete()
        return Response(message=f"Transaction {transaction_id} deleted", success=True)
    except Transaction.DoesNotExist:
        raise NotFound('Transaction not found')