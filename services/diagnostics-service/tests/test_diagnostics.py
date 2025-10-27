import importlib.util
import sys
from pathlib import Path

_MAIN_PATH = Path(__file__).resolve().parents[1] / "main.py"
_spec = importlib.util.spec_from_file_location("diagnostics_service_main", _MAIN_PATH)
_module = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _module
_spec.loader.exec_module(_module)
app = _module.app

from fastapi.testclient import TestClient

client = TestClient(app)

VALID_DTC = {
    "vehicle_id": "VIN-TEST-001",
    "code": "P0562",
    "severity": "medium",
    "description": "Low system voltage detected",
}


def test_health_returns_200():
    resp = client.get("/health")
    assert resp.status_code == 200


def test_post_diagnostics_accepts_valid_code():
    resp = client.post("/diagnostics", json=VALID_DTC)
    assert resp.status_code == 201
    assert resp.json()["code"] == "P0562"


def test_invalid_severity_is_rejected():
    payload = dict(VALID_DTC)
    payload["severity"] = "catastrophic"
    resp = client.post("/diagnostics", json=payload)
    assert resp.status_code == 422


def test_get_diagnostics_returns_list_for_vehicle():
    client.post("/diagnostics", json=VALID_DTC)
    resp = client.get("/diagnostics/VIN-TEST-001")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) >= 1


def test_unknown_vehicle_returns_404():
    resp = client.get("/diagnostics/UNKNOWN-VIN")
    assert resp.status_code == 404
