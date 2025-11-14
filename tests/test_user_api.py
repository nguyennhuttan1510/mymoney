import pytest
from django.contrib.auth.models import User

from tests.conftest import get_request
from tests.helper import create_user


# Arrange
@pytest.fixture
def user(db) -> User:
    return create_user(username="nguyennhuttan", password="123456", email="nguyentan15102000@gmail.com")


@pytest.mark.django_db
def test_user_register(client):
    request = get_request(client)
    res = request('post', '/api/auth/register', {"username": "nguyennhuttan", "password": "123456", "email": "nguyentan15102000@gmail.com"})
    print('res', res.json())
    assert res.status_code == 201
    assert res.json()["success"] == True


@pytest.mark.django_db
def test_unique_register(client, user: User):
    request = get_request(client)
    res = request('post', '/api/auth/register', {"username": user.username, "password": "123456", "email": user.email})
    assert res.status_code == 400
    assert res.json()["success"] == False


@pytest.mark.django_db
def test_user_login(client, user: User):
    request = get_request(client)
    res = request('post', '/api/auth/login', {"username": user.username, "password": "123456"})
    assert res.status_code == 200
    assert "access_token" in res.json()["data"]

