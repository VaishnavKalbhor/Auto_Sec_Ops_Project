import importlib.util
import sys
from pathlib import Path

_MAIN_PATH = Path(__file__).resolve().parents[1] / "main.py"
_spec = importlib.util.spec_from_file_location("telemetry_service_main", _MAIN_PATH)
_module = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _module
_spec.loader.exec_module(_module)
app = _module.app

from fastapi.testclient import TestClient

client = TestClient(app)

VALID_PAYLOAD = {
    "vehicle_id": "VIN-TEST-001",
    "speed": 80,
    "battery_level": 75,
    "temperature": 38.5,
    "software_version": "1.0.0",
}


def test_health_returns_200():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_post_telemetry_accepts_valid_payload():
    resp = client.post("/telemetry", json=VALID_PAYLOAD)
    assert resp.status_code == 201
    assert resp.json()["vehicle_id"] == "VIN-TEST-001"


def test_post_telemetry_rejects_missing_vehicle_id():
    payload = dict(VALID_PAYLOAD)
    del payload["vehicle_id"]
    resp = client.post("/telemetry", json=payload)
    assert resp.status_code == 422


def test_get_telemetry_returns_saved_data():
    client.post("/telemetry", json=VALID_PAYLOAD)
    resp = client.get("/telemetry/VIN-TEST-001")
    assert resp.status_code == 200
    assert resp.json()["speed"] == 80


def test_get_telemetry_unknown_vehicle_returns_404():
    resp = client.get("/telemetry/UNKNOWN-VIN")
    assert resp.status_code == 404
