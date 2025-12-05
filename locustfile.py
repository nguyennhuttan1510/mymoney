from locust import HttpUser, task, between
import json

# Thông tin JWT nếu cần login trước
USERNAME = "admin"
PASSWORD = "o0i9u8y7"

class ApiUser(HttpUser):
    wait_time = between(0.01, 0.05)  # thời gian chờ giữa các request

    def on_start(self):
        """
        Gọi khi user bắt đầu: đăng nhập và lưu JWT
        """
        response = self.client.post(
            "/api/auth/login",  # endpoint login của bạn
            json={"username": USERNAME, "password": PASSWORD}
        )
        if response.status_code == 200:
            self.token = response.json()['data']['access_token']  # token JWT
        else:
            self.token = None

    @task
    def call_protected_api(self):
        """
        Giả lập user gọi API protected
        """
        if not self.token:
            return

        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/api/transaction/", headers=headers)