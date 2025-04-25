import pytest
from ninja.testing import TestClient
# from mymoney.api import api
from transaction.models import Transaction

# client = TestClient(api)

@pytest.mark.django_db
def test_create_transaction_unit(client, admin_user):
    data = {
        "wallet_id": 1,
        "amount": 10000,
        "category_id": 3,
        "transaction_date": "2025-04-25T08:32:21.775Z"
    }
    response = client.post("/transaction/", data)
    assert response.status_code == 200
    assert response.json()["wallet_id"] == "1"
    assert response.json()["amount"] == "10000"
    assert Transaction.objects.count() == 1
#
# @pytest.mark.django_db
# def test_get_transaction_unit():
#     t = Transaction.objects.create(title="Lunch", amount=50, type="expense")
#     response = client.get(f"/transactions/{t.id}")
#     assert response.status_code == 200
#     assert response.json()["title"] == "Lunch"
