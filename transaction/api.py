
from django.core.exceptions import ObjectDoesNotExist
from ninja import Router, Query

from transaction.service import TransactionService
from core.schema.response import ResponseSchema, SuccessResponse, CreateSuccessResponse, BadRequestResponse, \
    NotFoundResponse
from services.auth_jwt import JWTAuth
from transaction.schema import TransactionOut, TransactionIn, TransactionUpdateSchema, TransactionQuery, \
    TransactionListOut

router = Router(tags=['Transaction'], auth=JWTAuth())


@router.post("/", response={201: ResponseSchema[TransactionOut], 400: ResponseSchema, 404: ResponseSchema})
def create_transaction(request, payload: TransactionIn):
    try:
        user = getattr(request, 'auth', None)
        transaction = TransactionService.process(action='create', payload=payload, user=user)
        return CreateSuccessResponse(data=transaction, message='Created transaction successfully')
    except Exception as e:
        return BadRequestResponse(message=f'Create failed - {str(e)}')


@router.get("/", response={200: ResponseSchema[TransactionListOut], 404: ResponseSchema})
def get_all_transaction(request, query: Query[TransactionQuery]):
    try:
        result = TransactionService.search(params=query)
        size_kb = len(result.model_dump_json().encode()) / 1024
        print('Size:', size_kb, "KB")
        return SuccessResponse(data=result,
                               message=f"Get all transactions of user {request.auth.pk} successfully")
    except Exception as e:
        return NotFoundResponse(message=f'Get transactions failed - {str(e)}')


@router.get("/{int:transaction_id}", response={200: ResponseSchema[TransactionOut], 404: ResponseSchema})
def get_transaction(request, transaction_id: int):
    try:
        transaction = TransactionService.repository.get_by_id(pk=transaction_id)
        return SuccessResponse(data=transaction, message=f'Get transaction {transaction_id} success')
    except ObjectDoesNotExist:
        return NotFoundResponse(f"Transaction with id {transaction_id} does not exist")


@router.patch("/{int:transaction_id}", response={200: ResponseSchema[TransactionOut], 400: ResponseSchema})
def update_transaction(request, transaction_id: int, payload: TransactionUpdateSchema):
    try:
        user = getattr(request, 'auth', None)
        transaction_updated = TransactionService.process(action='update', transaction_id=transaction_id,
                                                         payload=payload, user=user)
        return SuccessResponse(data=transaction_updated,
                               message=f"Updated transactions {transaction_id} of user {user.pk} successfully")
    except Exception as e:
        return BadRequestResponse(f'Updated transactions failed - {str(e)}')


@router.delete("/{int:transaction_id}", response=ResponseSchema)
def delete_transaction(request, transaction_id: int):
    try:
        user = getattr(request, 'auth', None)
        TransactionService.destroy(transaction_id, user=user)
        return SuccessResponse(message=f"Transaction {transaction_id} deleted", success=True)
    except Exception as e:
        print('e', e)
        return BadRequestResponse(f'Delete transaction {transaction_id} failed')
