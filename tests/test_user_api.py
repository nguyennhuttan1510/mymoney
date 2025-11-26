from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from ninja.testing import TestClient
from django.utils import timezone

from core.exceptions.session_exception import SessionInactive, SessionException, SessionExpired
from mymoney.api import api
from session.models import Session
from tests.conftest import get_request
from tests.helper import create_user


@pytest.mark.django_db
def test_user_register(client):
    request = get_request(client)
    res = request('post', '/api/auth/register',
                  {"username": "nguyennhuttan", "password": "123456", "email": "nguyentan15102000@gmail.com"})
    print('res', res.json())
    assert res.status_code == 201
    assert res.json()["success"] == True


@pytest.mark.django_db
def test_unique_register(client, create_user):
    user = create_user(username="nguyennhuttan", password="123456", email="nguyentan15102000@gmail.com")
    request = get_request(client)
    res = request('post', '/api/auth/register', {"username": user.username, "password": "123456", "email": user.email})
    assert res.status_code == 400
    assert res.json()["success"] == False


@pytest.mark.django_db
def test_user_login(client, create_user):
    user = create_user(username="nguyennhuttan", password="123456", email="nguyentan15102000@gmail.com")
    request = get_request(client)
    res = request('post', '/api/auth/login', {"username": user.username, "password": "123456"})
    assert res.status_code == 200
    assert "access_token" in res.json()["data"]
    assert "refresh_token" in res.json()["data"]


# session only exist until another login, system will create a new session, revoke old session
@pytest.mark.django_db
def test_session_only_existed_in_time(client, create_user):
    request = get_request(client)
    # Arrange
    user = create_user(username="client_01", password="123456", email="client_01@gmail.com")
    # Action - logic success the first and create session
    res = request('post', '/api/auth/login', {"username": user.username, "password": "123456"})
    assert res.status_code == 200
    first_sessions = Session.objects.filter(user=user, is_active=True).first()
    # Action - logic success the second and create new session and revoke old session of user
    request('post', '/api/auth/login', {"username": user.username, "password": "123456"})
    second_sessions = Session.objects.filter(user=user, is_active=True).first()
    assert first_sessions.session_id != second_sessions.session_id
    first_sessions.refresh_from_db()
    assert first_sessions.is_active == False


client_api = TestClient(api)


# -----------------------test session-----------------------------------
# session have been inactive is not access private url
@pytest.mark.django_db
def test_session_is_revoked_when_inactive(client, create_user):
    # Arrange
    user = create_user(username="client_01", password="123456", email="client_01@gmail.com")
    # Action - logic success -> session created
    res = client.post(path='/api/auth/login', data={"username": user.username, "password": "123456"},
                      content_type="application/json")
    # mockup session is inactive
    session = Session.objects.get(user=user, is_active=True)
    session.is_active = False
    session.save()
    # Action - access private url
    res = client.get('/api/transaction/', headers={"Authorization": f"Bearer {res.json()['data']['access_token']}"},
                     content_type="application/json")
    assert res.status_code == SessionInactive.status_code
    assert res.json()['error']['code'] == SessionInactive.error_code


# session not found will be rejected
@pytest.mark.django_db
def test_session_is_reject_when_session_not_found(client, create_user):
    # Arrange
    user = create_user(username="client_01", password="123456", email="client_01@gmail.com")
    # Action - logic success -> session created
    res = client.post(path='/api/auth/login', data={"username": user.username, "password": "123456"},
                      content_type="application/json")
    # mockup session not found
    session = Session.objects.get(user=user, is_active=True)
    session.delete()
    session.save()
    # Action - access private url
    res = client.get('/api/transaction/', headers={"Authorization": f"Bearer {res.json()['data']['access_token']}"},
                     content_type="application/json")
    assert res.status_code == SessionException.status_code
    assert res.json()['error']['code'] == SessionException.error_code

# ----------------------------------------------------------------------------
