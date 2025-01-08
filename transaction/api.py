from ninja import Router, NinjaAPI

from transaction.models import Transaction
from transaction.schema import TransactionSchema

router = Router()

@router.post("/")
def create_transaction(request, payload: TransactionSchema ):
    transaction = Transaction.objects.create(**payload.dict())
    # return {"message": "Transaction created successfully"}
    return transaction