import pytest
import requests
from config.settings import BASE_URL


@pytest.mark.smoke
def test_service_is_up():
    assert requests.get(f"{BASE_URL}/health", timeout=5).status_code == 200
