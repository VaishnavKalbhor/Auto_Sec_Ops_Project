"""
Vehicle event simulator.

Simulates a single connected vehicle going through a realistic flow:
1. Register the vehicle in the Vehicle Registry Service
2. Send a telemetry reading to the Telemetry Service
3. Send a diagnostic trouble code to the Diagnostics Service

Run this against live services, e.g. after `docker compose up --build`:

    python scripts/generate_vehicle_events.py

Service base URLs can be overridden via environment variables:
    REGISTRY_URL   (default http://localhost:8002)
    TELEMETRY_URL  (default http://localhost:8001)
    DIAGNOSTICS_URL (default http://localhost:8003)
"""
import os
import sys

import httpx

REGISTRY_URL = os.environ.get("REGISTRY_URL", "http://localhost:8002")
TELEMETRY_URL = os.environ.get("TELEMETRY_URL", "http://localhost:8001")
DIAGNOSTICS_URL = os.environ.get("DIAGNOSTICS_URL", "http://localhost:8003")

VEHICLE = {
    "vehicle_id": "VIN-TEST-001",
    "model": "EV-Test-X",
    "owner_type": "fleet",
    "region": "EU",
    "software_version": "1.2.0",
}

TELEMETRY_EVENT = {
    "vehicle_id": "VIN-TEST-001",
    "speed": 82,
    "battery_level": 67,
    "temperature": 39.5,
    "software_version": "1.2.0",
}

DIAGNOSTIC_EVENT = {
    "vehicle_id": "VIN-TEST-001",
    "code": "P0562",
    "severity": "medium",
    "description": "Low system voltage detected",
}


def main() -> int:
    with httpx.Client(timeout=10.0) as client:
        resp = client.post(f"{REGISTRY_URL}/vehicles", json=VEHICLE)
        if resp.status_code not in (201, 409):
            print(f"Failed to create vehicle: {resp.status_code} {resp.text}")
            return 1
        print(f"Created vehicle {VEHICLE['vehicle_id']}")

        resp = client.post(f"{TELEMETRY_URL}/telemetry", json=TELEMETRY_EVENT)
        if resp.status_code != 201:
            print(f"Failed to send telemetry: {resp.status_code} {resp.text}")
            return 1
        print("Sent telemetry event")

        resp = client.post(f"{DIAGNOSTICS_URL}/diagnostics", json=DIAGNOSTIC_EVENT)
        if resp.status_code != 201:
            print(f"Failed to send diagnostic: {resp.status_code} {resp.text}")
            return 1
        print(f"Sent diagnostic code {DIAGNOSTIC_EVENT['code']}")

    print("Vehicle flow completed successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
