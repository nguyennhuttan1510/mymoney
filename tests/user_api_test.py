import pytest
from httpx import AsyncClient


@pytest.mark.django_db
def test_user_login(client):
    res = client.post('/api/auth/login', json={"username":"nguyennhuttan", "password":"123456"}, content_type="application/json")
    print('res', res.json())
    assert res.status_code == 200
    assert "access_token" in res.json()["data"]