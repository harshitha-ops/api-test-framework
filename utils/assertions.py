from jsonschema import validate


def assert_status(resp, expected: int):
    assert resp.status_code == expected, (
        f"Expected {expected}, got {resp.status_code}. Body: {resp.text[:300]}")


def assert_schema(body: dict, schema: dict):
    validate(instance=body, schema=schema)
