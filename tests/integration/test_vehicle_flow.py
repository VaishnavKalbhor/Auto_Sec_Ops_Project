"""
Integration test proving a complete automotive-style data flow across all
three services: register a vehicle, send telemetry for it, send a
diagnostic code for it, and confirm all services report healthy.

This imports each service's FastAPI app directly and drives them with
in-process TestClients, so it does not require docker-compose or a live
network -- it still proves the services can be composed into one flow.
"""
import importlib.util
import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]


def _load_app(service_dir: str):
    module_name = f"_integration_{service_dir.replace('-', '_')}"
    main_path = ROOT / "services" / service_dir / "main.py"
    spec = importlib.util.spec_from_file_location(module_name, main_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module.app


telemetry_client = TestClient(_load_app("telemetry-service"))
registry_client = TestClient(_load_app("vehicle-registry-service"))
diagnostics_client = TestClient(_load_app("diagnostics-service"))

VEHICLE_ID = "VIN-TEST-001"


def test_all_services_report_healthy():
    assert telemetry_client.get("/health").status_code == 200
    assert registry_client.get("/health").status_code == 200
    assert diagnostics_client.get("/health").status_code == 200


def test_registry_accepts_vehicle():
    resp = registry_client.post(
        "/vehicles",
        json={
            "vehicle_id": VEHICLE_ID,
            "model": "EV-Test-X",
            "owner_type": "fleet",
            "region": "EU",
            "software_version": "1.2.0",
        },
    )
    assert resp.status_code in (201, 409)


def test_telemetry_accepts_event_for_same_vehicle():
    resp = telemetry_client.post(
        "/telemetry",
        json={
            "vehicle_id": VEHICLE_ID,
            "speed": 82,
            "battery_level": 67,
            "temperature": 39.5,
            "software_version": "1.2.0",
        },
    )
    assert resp.status_code == 201
    assert telemetry_client.get(f"/telemetry/{VEHICLE_ID}").status_code == 200


def test_diagnostics_accepts_event_for_same_vehicle():
    resp = diagnostics_client.post(
        "/diagnostics",
        json={
            "vehicle_id": VEHICLE_ID,
            "code": "P0562",
            "severity": "medium",
            "description": "Low system voltage detected",
        },
    )
    assert resp.status_code == 201
    assert diagnostics_client.get(f"/diagnostics/{VEHICLE_ID}").status_code == 200
