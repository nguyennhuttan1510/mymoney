from typing import List

from django.contrib.messages import success
from django.core.exceptions import BadRequest
from django.db import transaction as transaction_db
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from ninja import Router, NinjaAPI
from ninja import PatchDict
from ninja.responses import Response as ResponseNinja
from ninja.errors import ValidationError, Throttled
from ninja.responses import JsonResponse
from rest_framework.exceptions import NotFound

from budget.models import Budget
from category.models import Category
from core.exceptions.exceptions import ServerError
from core.models.transactions import SpendingTransaction
from core.schema.response import ResponseSchema, BaseResponse, SuccessResponse, ResponseAPI
from services.auth_jwt import JWTAuth
from transaction.models import Transaction
from transaction.schema import TransactionSchema, TransactionCreateSchema, TransactionUpdateSchema
from utils.query import query_or_not
from wallet.models import Wallet

router = Router(tags=['Transaction'], auth=JWTAuth())

@router.post("/", response={200: ResponseSchema[TransactionSchema], 400: ResponseSchema, 404: ResponseSchema})
def create_transaction(request, payload: TransactionCreateSchema ):
    try:
        with transaction_db.atomic():
            user = getattr(request, 'auth', None)
            category = query_or_not(Category, pk=payload.category)
            wallet = query_or_not(Wallet, pk=payload.wallet, user=user)
            budget = query_or_not(Budget, pk=payload.budget, user=user)

            transaction_data = {**payload.dict(), "category": category, "wallet": wallet, "budget": budget}
            transaction = SpendingTransaction(Transaction(user=user, **transaction_data))

            result = transaction.pay()

            return BaseResponse(data=result, message='Created transaction successfully')
    except Exception as e:
        print('e', e)
        raise Exception('Create failed')


@router.get("/", response=ResponseSchema[List[TransactionSchema]])
def get_all_transaction(request):
    transactions = Transaction.objects.filter(user=request.user)
    return ResponseAPI(SuccessResponse(data=transactions, message=f"Get all transactions of user {request.user.pk} successfully"))


@router.get("/{int:transaction_id}", response={200: ResponseSchema[TransactionSchema], 404: ResponseSchema[TransactionSchema]})
def get_transaction(request, transaction_id: int):
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        print('transaction', transaction)
        return ResponseAPI(SuccessResponse(data=transaction))
    except Transaction.DoesNotExist:
        raise NotFound(f"Transaction with id {transaction_id} does not exist")


@router.put("/{int:transaction_id}", response=ResponseSchema[TransactionSchema])
def update_transaction(request, transaction_id: int, payload: TransactionUpdateSchema):
    try:
        transaction_instance: Transaction = query_or_not(Transaction, id=transaction_id)

        wallet = query_or_not(Wallet, id=payload.get('wallet_id'))
        category = query_or_not(Category, id=payload.get('category_id'))

        transaction_instance.wallet = wallet
        transaction_instance.category = category
        transaction_instance.amount = payload.get('amount')

        transaction = SpendingTransaction(transaction_instance)
        transaction.pay()

        return ResponseAPI(SuccessResponse(data=transaction_instance, message=f"Updated transactions {transaction_instance.pk} of user {request.user.pk} successfully"))

    except Exception as e:
        raise BadRequest(f'Updated transactions failed')


@router.delete("/{int:transaction_id}", response=ResponseSchema)
def delete_transaction(request, transaction_id: int):
    try:
        transaction_instance = Transaction.objects.get(id=transaction_id, user=request.user)
        transaction_instance.delete()
        return BaseResponse(message=f"Transaction {transaction_id} deleted", success=True)
    except Transaction.DoesNotExist:
        raise NotFound('Transaction not found')