# E2E Notes

Run E2E sync test (skipped by default):

```bash
export RUN_E2E=1
export APP_URL=http://localhost:5000
export APP_SHARED_PASSWORD=changeme
python -m playwright install
pytest backend/tests/e2e/test_sync_two_clients.py
```

Requires app running and Playwright browsers installed.
