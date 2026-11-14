import pytest
from clients.users_client import UsersClient
from config.settings import TENANTS
from utils.data_factory import user_payload


@pytest.fixture(scope="session")
def acme():
    return UsersClient(TENANTS["acme"])


@pytest.fixture(scope="session")
def globex():
    return UsersClient(TENANTS["globex"])


@pytest.fixture
def created_user(acme):
    """Arrange step shared by tests; API-level setup keeps tests fast."""
    resp = acme.create_user(user_payload())
    assert resp.status_code == 201
    return resp.json()
