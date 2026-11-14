import pytest
from schemas.user_schema import USER_SCHEMA
from utils.assertions import assert_schema, assert_status
from utils.data_factory import user_payload


@pytest.mark.smoke
@pytest.mark.regression
def test_create_user_returns_201_and_valid_schema(acme):
    payload = user_payload()
    resp = acme.create_user(payload)
    assert_status(resp, 201)
    body = resp.json()
    assert_schema(body, USER_SCHEMA)
    assert body["email"] == payload["email"]
    assert body["tenant"] == "acme"


@pytest.mark.regression
def test_get_user_returns_created_user(acme, created_user):
    resp = acme.get_user(created_user["id"])
    assert_status(resp, 200)
    assert resp.json() == created_user  # POST -> GET round trip


@pytest.mark.regression
def test_list_users_contains_created_user(acme, created_user):
    resp = acme.list_users()
    assert_status(resp, 200)
    assert created_user["id"] in [u["id"] for u in resp.json()]


@pytest.mark.regression
def test_get_unknown_user_returns_404(acme):
    assert_status(acme.get_user("does-not-exist"), 404)


@pytest.mark.regression
@pytest.mark.parametrize("bad_payload", [
    {},
    {"name": "No Email"},
    {"email": "noname@example.com"},
    {"name": "Bad Email", "email": "not-an-email"},
], ids=["empty", "missing-email", "missing-name", "invalid-email"])
def test_create_user_validation_errors_return_400(acme, bad_payload):
    assert_status(acme.create_user(bad_payload), 400)


@pytest.mark.regression
def test_duplicate_email_in_same_tenant_returns_409(acme):
    payload = user_payload()
    assert_status(acme.create_user(payload), 201)
    assert_status(acme.create_user(payload), 409)


@pytest.mark.regression
def test_same_email_allowed_across_tenants(acme, globex):
    payload = user_payload()
    assert_status(acme.create_user(payload), 201)
    assert_status(globex.create_user(payload), 201)
