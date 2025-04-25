import pytest
from django.contrib.auth.models import User
from mymoney.api import api
from ninja.testing import TestClient

@pytest.fixture
def admin_user(db):
    return User.objects.create_user(username="admin", password="o0i9u8y7")

@pytest.fixture
def client():
    return TestClient(api)
