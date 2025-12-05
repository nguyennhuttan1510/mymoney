from locust import HttpUser, task, between
import json

# Thông tin JWT nếu cần login trước
USERNAME = "admin"
PASSWORD = "o0i9u8y7"


import threading

token_lock = threading.Lock()
cached_token = None

def get_global_token(client):
    global cached_token
    with token_lock:
        if cached_token is None:
            res = client.post(
                "/api/auth/login",
                json={"username": USERNAME, "password": PASSWORD}
            )
            if res.status_code == 200:
                cached_token = res.json()["data"]["access_token"]
        return cached_token


class ApiUser(HttpUser):
    wait_time = between(1, 3)  # thời gian chờ giữa các request

    def on_start(self):
        """
        Gọi khi user bắt đầu: đăng nhập và lưu JWT
        """
        self.token = get_global_token(self.client)

    @task
    def call_protected_api(self):
        """
        Giả lập user gọi API protected
        """
        if not self.token:
            return

        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/api/transaction/", headers=headers)