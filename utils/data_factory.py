import uuid


def user_payload(**overrides) -> dict:
    """Unique data per call -> tests are independent and parallel-safe."""
    suffix = uuid.uuid4().hex[:8]
    data = {"name": f"QA User {suffix}", "email": f"qa_{suffix}@example.com"}
    data.update(overrides)
    return data
