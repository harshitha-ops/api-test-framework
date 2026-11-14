import os

ENVIRONMENTS = {
    "local": "http://localhost:5001",
    "staging": "https://staging.example.com",
}
ENV = os.getenv("TEST_ENV", "local")
BASE_URL = os.getenv("BASE_URL", ENVIRONMENTS[ENV])
TIMEOUT = float(os.getenv("API_TIMEOUT", "10"))
# Secrets come from env vars / CI secrets, never from code
TENANTS = {
    "acme": {"id": "acme", "api_key": os.getenv("ACME_KEY", "key-acme")},
    "globex": {"id": "globex", "api_key": os.getenv("GLOBEX_KEY", "key-globex")},
}
