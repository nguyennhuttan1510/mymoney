from typing import List

from django.db import transaction as transaction_db
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from ninja import Router, NinjaAPI
from ninja import PatchDict
from rest_framework.exceptions import NotFound

from budget.models import Budget
from category.models import Category
from core.models.transactions import SpendingTransaction
from core.schema.response import ResponseSchema, Response
from services.auth_jwt import JWTAuth
from transaction.models import Transaction
from transaction.schema import TransactionSchema, TransactionCreateSchema
from utils.query import query_or_not
from wallet.models import Wallet

router = Router(tags=['Transaction'], auth=JWTAuth())

@router.post("/", response=ResponseSchema[TransactionSchema])
def create_transaction(request, payload: TransactionCreateSchema ):
    try:
        with transaction_db.atomic():
            user = getattr(request, 'auth', None)
            category = query_or_not(Category, pk=payload.category)
            if category is None: raise Category.DoesNotExist
            wallet = query_or_not(Wallet, pk=payload.wallet, user=user)
            budget = query_or_not(Budget, pk=payload.budget, user=user)

            transaction_data = {**payload.dict(), "category": category, "wallet": wallet, "budget": budget}
            transaction = SpendingTransaction(Transaction(user=user, **transaction_data))

            result = transaction.pay()

            return Response(data=result, message='Created transaction successfully' )
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
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        print('transaction', transaction)
        if transaction is None:
            raise HttpResponseBadRequest()
        return Response(data=transaction, message=f"Get transactions {transaction.pk} successfully" )
    except Exception as e:
        print('e', e)
        return Response(message=f"Transaction with id {transaction_id} does not exist")


@router.put("/{int:transaction_id}", response=ResponseSchema[TransactionSchema])
def update_transaction(request, transaction_id: int, item: PatchDict[TransactionCreateSchema]):
    try:
        transaction_instance = get_object_or_404(Transaction, id=transaction_id)
        for key, value in item.items():
            if value is not None:
                if key == 'category':
                    category = Category.objects.get(pk=value)
                    value = category
                if key == 'wallet':
                    wallet = Wallet.objects.get(pk=value)
                    value = wallet
                setattr(transaction_instance, key, value)

        transaction = SpendingTransaction(transaction_instance)
        transaction.pay()



        return Response(data=transaction_instance, message=f"Updated transactions {transaction_instance.pk} of user {request.user.pk} successfully" )

    except Transaction.DoesNotExist:
        return Response(message=f"Transaction with id {id} does not exist" )


@router.delete("/{int:transaction_id}", response=ResponseSchema)
def delete_transaction(request, transaction_id: int):
    try:
        transaction_instance = Transaction.objects.get(id=transaction_id, user=request.user)
        transaction_instance.delete()
        return Response(message=f"Transaction {transaction_id} deleted", success=True)
    except Transaction.DoesNotExist:
        raise NotFound('Transaction not found')