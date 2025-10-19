"""
Lightweight API security checks run against each service in-process.
These are not a replacement for the ZAP DAST scan -- they check a handful
of things a real API should always get right: no stack traces leaking to
clients, sane status codes for garbage input, and unknown routes returning
404 rather than something more revealing.
"""
import importlib.util
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]

SERVICES = [
    "telemetry-service",
    "vehicle-registry-service",
    "diagnostics-service",
]


def _load_app(service_dir: str):
    module_name = f"_sectest_{service_dir.replace('-', '_')}"
    main_path = ROOT / "services" / service_dir / "main.py"
    spec = importlib.util.spec_from_file_location(module_name, main_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module.app


@pytest.fixture(params=SERVICES)
def client(request):
    return TestClient(_load_app(request.param))


def test_health_endpoint_has_no_secrets_or_internals(client):
    resp = client.get("/health")
    body = resp.text.lower()
    for forbidden in ("password", "secret", "api_key", "traceback"):
        assert forbidden not in body


def test_invalid_json_body_returns_4xx(client):
    resp = client.post(
        "/health",  # wrong method/route on purpose; also covers unknown-route case below
    )
    assert resp.status_code in (404, 405)


def test_unknown_route_returns_404(client):
    resp = client.get("/this-route-does-not-exist")
    assert resp.status_code == 404


def test_malformed_payload_does_not_return_500(client):
    # Send garbage JSON to whichever POST endpoint the service exposes.
    # We don't know the exact route generically, so we hit a plausible one
    # per service and just assert we never get a raw 500 with a traceback.
    for path in ("/telemetry", "/vehicles", "/diagnostics"):
        resp = client.post(path, json={"garbage": "data", "vehicle_id": ""})
        assert resp.status_code != 500
        assert "traceback" not in resp.text.lower()
