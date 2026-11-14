"""Tiny multi-tenant REST API used as the system under test (SUT).
Run: python mock_app/app.py   -> http://localhost:5001
Swap BASE_URL in config to point at a real service instead."""
import uuid
from flask import Flask, jsonify, request

app = Flask(__name__)
API_KEYS = {"key-acme": "acme", "key-globex": "globex"}  # api key -> tenant
USERS = {}  # user_id -> dict


def _tenant():
    key = request.headers.get("X-API-Key")
    tenant = API_KEYS.get(key)
    if not tenant:
        return None, (jsonify(error="unauthorized"), 401)
    if request.headers.get("X-Tenant-ID") != tenant:
        return None, (jsonify(error="tenant mismatch"), 403)
    return tenant, None


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.post("/api/v1/users")
def create_user():
    tenant, err = _tenant()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    name, email = body.get("name"), body.get("email")
    if not name or not email or "@" not in email:
        return jsonify(error="name and valid email required"), 400
    if any(u["tenant"] == tenant and u["email"] == email for u in USERS.values()):
        return jsonify(error="email already exists"), 409
    uid = str(uuid.uuid4())
    USERS[uid] = {"id": uid, "name": name, "email": email, "tenant": tenant}
    return jsonify(USERS[uid]), 201


@app.get("/api/v1/users/<uid>")
def get_user(uid):
    tenant, err = _tenant()
    if err:
        return err
    user = USERS.get(uid)
    if not user or user["tenant"] != tenant:  # never leak cross-tenant existence
        return jsonify(error="not found"), 404
    return jsonify(user), 200


@app.get("/api/v1/users")
def list_users():
    tenant, err = _tenant()
    if err:
        return err
    return jsonify([u for u in USERS.values() if u["tenant"] == tenant]), 200


if __name__ == "__main__":
    app.run(port=5001)
