from core.models.transactions import TransactionService
from transaction.schema import TransactionCreateSchema, TransactionUpdateSchema
from utils import repository as repository_transaction


def create_transaction(data: TransactionCreateSchema, user_id):
    payload_transaction = {**data.dict(by_alias=True), 'user_id': user_id}
    transaction = TransactionService.process(payload=payload_transaction)
    return transaction


def get_all_transaction(user_id):
    return repository_transaction.get_all(user_id)


def update_transaction(transaction_id: int, data: TransactionUpdateSchema, user_id:int):
    transaction_updated = repository_transaction.get_by_id(transaction_id)
    for field, value in data.dict().items():
        if value is not None:
            setattr(transaction_updated, field, value)
    payload_transaction = {**TransactionCreateSchema.from_orm(transaction_updated).dict(by_alias=True), 'user_id': user_id}
    return TransactionService.execute(action='modify', payment_method='cash', transaction_id=transaction_id, payload_transaction=payload_transaction, user_id=user_id)


def delete_transaction(transaction_id: int, user_id: int):
    # TransactionService.execute('cancel', payment_method='cash', transaction_id=transaction_id, user_id=user_id)
    transaction = repository_transaction.get_by_id(transaction_id)
    TransactionService.destroy(transaction_id)
