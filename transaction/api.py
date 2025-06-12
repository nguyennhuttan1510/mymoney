from typing import List

from ninja import Router
from rest_framework.exceptions import NotFound

from core.exceptions.exceptions import BadRequest
from core.models.transactions import TransactionService
# from core.models.transactions import SpendingTransaction
from core.schema.response import ResponseSchema, BaseResponse, SuccessResponse, CreateSuccessResponse
from services.auth_jwt import JWTAuth
from transaction.models import Transaction
from transaction.schema import TransactionSchema, TransactionCreateSchema, TransactionUpdateSchema
# from transaction.service import TransactionService
from transaction import service

router = Router(tags=['Transaction'], auth=JWTAuth())

@router.post("/", response={201: ResponseSchema[TransactionSchema], 400: ResponseSchema, 404: ResponseSchema})
def create_transaction(request, payload: TransactionCreateSchema ):
    user = getattr(request, 'auth', None)
    TransactionService.process(payload, user)
    # return CreateSuccessResponse(data=res, message='Created transaction successfully')

@router.get("/", response=ResponseSchema[List[TransactionSchema]])
def get_all_transaction(request):
    user = getattr(request, 'auth', None)

    res = service.get_all_transaction(user_id=user.pk)
    return SuccessResponse(data=res, message=f"Get all transactions of user {request.user.pk} successfully")


@router.get("/{int:transaction_id}", response={200: ResponseSchema[TransactionSchema], 404: ResponseSchema[TransactionSchema]})
def get_transaction(request, transaction_id: int):
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        return SuccessResponse(data=transaction)
    except Transaction.DoesNotExist:
        raise NotFound(f"Transaction with id {transaction_id} does not exist")


@router.patch("/{int:transaction_id}", response=ResponseSchema[TransactionSchema])
def update_transaction(request, transaction_id: int, payload: TransactionUpdateSchema):
    try:
        user = getattr(request, 'auth', None)
        res = service.update_transaction(transaction_id, data=payload, user_id=user.pk)
        return SuccessResponse(data=res, message=f"Updated transactions {transaction_id} of user {user.pk} successfully")

    except Exception as e:
        print('e', e)
        raise BadRequest(f'Updated transactions failed')


@router.delete("/{int:transaction_id}", response=ResponseSchema)
def delete_transaction(request, transaction_id: int):
    try:
        user = getattr(request, 'auth', None)
        service.delete_transaction(transaction_id, user_id = user.pk)
        return BaseResponse(message=f"Transaction {transaction_id} deleted", success=True)
    except Exception as e:
        print('e', e)
        raise BadRequest(f'Delete transaction {transaction_id} failed')