import os

os.environ["ATLAS_DATABASE_URL"] = "sqlite://"

from fastapi.testclient import TestClient

from app.main import app
from app.security import create_access_token
from app.services.metrics import summarize_usage

client = TestClient(app)
AUTH_HEADERS = {"Authorization": f"Bearer {create_access_token('tester@atlas')}"}


def test_live():
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_current_tenant_default():
    response = client.get("/tenants/current")
    assert response.status_code == 200
    payload = response.json()
    assert payload["tenant"] == "demo"
    assert "usage" in payload


def test_catalog_lists_datasets():
    response = client.get("/tenants/demo/catalog")
    assert response.status_code == 200
    datasets = response.json()
    assert isinstance(datasets, list)
    assert datasets[0]["name"] == "knowledge_base"


def test_upsert_and_update_usage_flow():
    upsert = client.post(
        "/tenants",
        json={"tenant": "globex", "plan": "growth"},
        headers=AUTH_HEADERS,
    )
    assert upsert.status_code == 200
    assert upsert.json()["usage"]["plan"] == "growth"

    usage = client.post(
        "/tenants/globex/usage",
        json={"tokens_delta": 5000, "requests_delta": 10},
        headers=AUTH_HEADERS,
    )
    assert usage.status_code == 200
    assert usage.json()["usage"]["tokens"] == 5000


def test_billing_preview_endpoint():
    response = client.get("/billing/demo/preview")
    assert response.status_code == 200
    payload = response.json()
    assert payload["tenant"] == "demo"
    assert payload["plan"] == "scale"


def test_metrics_event_flow():
    response = client.post(
        "/metrics/usage",
        json={"tenant": "demo", "source": "test", "tokens": 123, "latency_ms": 100.5},
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 202
    summary = client.get("/metrics/usage/daily", headers=AUTH_HEADERS).json()
    assert any(item["tenant"] == "demo" for item in summary)


def test_auth_token_endpoint():
    response = client.post("/auth/token", json={"username": "admin@atlas", "password": "atlas"})
    assert response.status_code == 200
    payload = response.json()
    assert "access_token" in payload
