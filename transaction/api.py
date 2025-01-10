from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router, NinjaAPI
from ninja import PatchDict

from category.models import Category
from core.schema.response import ResponseSchema, Response
from services.auth_jwt import JWTAuth
from transaction.models import Transaction
from transaction.schema import TransactionSchema, TransactionCreateSchema

router = Router(tags=['Transaction'], auth=JWTAuth())

@router.post("/", response=ResponseSchema[TransactionSchema])
def create_transaction(request, payload: TransactionCreateSchema ) -> ResponseSchema[TransactionSchema]:
    try:
        user = getattr(request, 'user', None)
        category = Category.objects.get(pk=payload.category)
        transaction_data = {**payload.dict(), "category": category}
        transaction = Transaction.objects.create(user=user ,**transaction_data)
        return Response(data=transaction, message='Created transaction successfully' )
    except Category.DoesNotExist:
        return Response(message=f"Category with id {payload.category} does not exist" )
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
                setattr(transaction, key, value)

        transaction.save()
        return Response(data=transaction, message=f"Updated transactions {transaction.pk} of user {request.user.pk} successfully" )

    except Transaction.DoesNotExist:
        return Response(message=f"Transaction with id {id} does not exist" )


@router.delete("/{int:transaction_id}", response=ResponseSchema)
def delete_employee(request, transaction_id: int):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.delete()
    return Response(message=f"Transaction {transaction_id} deleted", success=True)