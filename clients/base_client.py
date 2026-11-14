from __future__ import annotations
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.settings import BASE_URL, TIMEOUT

log = logging.getLogger("api")


class BaseClient:
    """Single place for session, headers, timeouts, logging, retries."""

    def __init__(self, tenant: dict | None = None, api_key: str | None = None):
        self.session = requests.Session()
        retry = Retry(total=2, backoff_factor=0.3, status_forcelist=[502, 503, 504])
        self.session.mount("http://", HTTPAdapter(max_retries=retry))
        self.session.mount("https://", HTTPAdapter(max_retries=retry))
        if tenant:
            self.session.headers["X-Tenant-ID"] = tenant["id"]
            self.session.headers["X-API-Key"] = api_key or tenant["api_key"]

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{BASE_URL}{path}"
        resp = self.session.request(method, url, timeout=TIMEOUT, **kwargs)
        log.info("%s %s -> %s (%.0f ms)", method, url, resp.status_code,
                 resp.elapsed.total_seconds() * 1000)
        return resp
