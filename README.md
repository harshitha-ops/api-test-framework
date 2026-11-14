# Multi-tenant API Test Framework (pytest + requests)

## Run
```
pip install -r requirements.txt
python mock_app/app.py &          # sample multi-tenant API on :5000
pytest -m smoke                   # fast gate
pytest -n 4                       # full suite in parallel
# real service: BASE_URL=https://staging.example.com ACME_KEY=... GLOBEX_KEY=... pytest
```
Reports: `reports/report.html`, `reports/junit.xml`

## Layers
config -> clients (service layer) -> tests; utils (assertions, schema, data factory); CI in `.github/workflows`.
See `architecture.png`.

## Scaling
Parallel (xdist), Docker, env/tenant config via env vars, markers for suites, independent test data, CI gates (smoke on PR, full nightly).
