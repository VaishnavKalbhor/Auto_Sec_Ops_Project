import importlib.util
import sys
from pathlib import Path

_MAIN_PATH = Path(__file__).resolve().parents[1] / "main.py"
_spec = importlib.util.spec_from_file_location("registry_service_main", _MAIN_PATH)
_module = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _module
_spec.loader.exec_module(_module)
app = _module.app

from fastapi.testclient import TestClient

client = TestClient(app)

VALID_VEHICLE = {
    "vehicle_id": "VIN-TEST-001",
    "model": "EV-Test-X",
    "owner_type": "fleet",
    "region": "EU",
    "software_version": "1.2.0",
}


def test_health_returns_200():
    resp = client.get("/health")
    assert resp.status_code == 200


def test_post_vehicles_creates_vehicle():
    resp = client.post("/vehicles", json=VALID_VEHICLE)
    assert resp.status_code == 201
    assert resp.json()["vehicle_id"] == "VIN-TEST-001"


def test_get_vehicles_returns_list():
    client.post("/vehicles", json=VALID_VEHICLE)
    resp = client.get("/vehicles")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) >= 1


def test_get_vehicle_by_id_returns_one_vehicle():
    client.post("/vehicles", json=VALID_VEHICLE)
    resp = client.get("/vehicles/VIN-TEST-001")
    assert resp.status_code == 200
    assert resp.json()["model"] == "EV-Test-X"


def test_duplicate_vehicle_id_is_rejected():
    client.post("/vehicles", json=VALID_VEHICLE)
    resp = client.post("/vehicles", json=VALID_VEHICLE)
    assert resp.status_code == 409


def test_invalid_region_is_rejected():
    payload = dict(VALID_VEHICLE)
    payload["vehicle_id"] = "VIN-TEST-002"
    payload["region"] = "MARS"
    resp = client.post("/vehicles", json=payload)
    assert resp.status_code == 422
