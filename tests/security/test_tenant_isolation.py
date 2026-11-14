import pytest
from clients.users_client import UsersClient
from config.settings import TENANTS
from utils.assertions import assert_status


@pytest.mark.security
def test_tenant_cannot_read_other_tenants_user(globex, created_user):
    """created_user belongs to acme; globex must get 404 (no existence leak)."""
    assert_status(globex.get_user(created_user["id"]), 404)


@pytest.mark.security
def test_list_never_returns_other_tenants_data(globex, created_user):
    resp = globex.list_users()
    assert_status(resp, 200)
    assert created_user["id"] not in [u["id"] for u in resp.json()]


@pytest.mark.security
def test_missing_api_key_returns_401():
    client = UsersClient(TENANTS["acme"])
    client.session.headers.pop("X-API-Key")
    assert_status(client.list_users(), 401)


@pytest.mark.security
def test_tenant_header_spoofing_returns_403():
    """acme's key + globex's tenant id must be rejected."""
    client = UsersClient({"id": "globex", "api_key": TENANTS["acme"]["api_key"]})
    assert_status(client.list_users(), 403)
