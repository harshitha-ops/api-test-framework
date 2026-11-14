from clients.base_client import BaseClient


class UsersClient(BaseClient):
    """Service layer: one method per endpoint. Tests never build URLs."""

    def create_user(self, payload: dict):
        return self.request("POST", "/api/v1/users", json=payload)

    def get_user(self, user_id: str):
        return self.request("GET", f"/api/v1/users/{user_id}")

    def list_users(self):
        return self.request("GET", "/api/v1/users")
