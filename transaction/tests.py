from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from ninja.testing import TestClient

from transaction.api import router as transaction_router
from utils.common import TransactionType
from wallet.models import Wallet


# Create your tests here.
class TransactionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='client_01', password='o0i9u8y7',
                                                            email='client_01@gmail.com')

        self.user_1 = User.objects.create_user(username='client_02', password='o0i9u8y7',
                                             email='client_02@gmail.com')

        self.access_token = self.get_access_token(self.user)
        self.access_token_1 = self.get_access_token(self.user_1)

        self.wallet = Wallet.objects.create(name='Main', balance=1000000, user=self.user, type='cash')
        self.wallet_2 = Wallet.objects.create(name='Second', balance=500000, user=self.user, type='cash')
        self.wallet_3 = Wallet.objects.create(name='Test', balance=500000, user=self.user, type='cash')

        self.client = TestClient(transaction_router)

    @staticmethod
    def get_access_token(user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    @staticmethod
    def get_header(access_token):
        return {"Authorization": f"Bearer {access_token}"}


    def test_create_transaction(self):
        payload = {
            'amount': 100000,
            'transaction_type': TransactionType.EXPENSE.value,
            'wallet_id': self.wallet.pk,
            'category_id': 1
        }
        response = self.client.post('/', json=payload, headers=self.get_header(self.access_token))
        self.assertEqual(response.status_code, 200)
        return response


    def test_update_transactions(self):
        transaction = self.test_create_transaction()

        payload = {
            'amount': 400000,
            'category_id': 2
        }
        response = self.client.put(f'/{transaction.data["data"]["id"]}', json=payload, headers=self.get_header(self.access_token))
        self.assertEqual(response.status_code, 200)


    def test_update_transaction_by_change_wallet(self):
        response_transaction = self.test_create_transaction()
        payload_change = {
            'wallet': self.wallet_2.pk,
        }
        self.client.put(f'/{response_transaction.data["data"]["id"]}', json=payload_change, headers=self.get_header(self.access_token))

    def test_balance_wallet_after_create_transaction(self):
        self.test_create_transaction()

        wallet = Wallet.objects.get(id=self.wallet.pk)
        self.assertEqual(wallet.balance, 900000)


    def test_wallet_balance_after_update_transaction(self):
        self.test_update_transactions()

        wallet = Wallet.objects.get(id=self.wallet.pk)
        self.assertEqual(wallet.balance, 600000)


    def test_wallet_balance_after_change_wallet(self):
        self.test_update_transaction_by_change_wallet()

        wallet = Wallet.objects.get(id=self.wallet.pk)
        wallet_2 = Wallet.objects.get(id=self.wallet_2.pk)

        self.assertEqual(wallet.balance, 1000000)
        self.assertEqual(wallet_2.balance, 400000)


