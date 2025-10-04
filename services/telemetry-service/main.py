"""
Telemetry Service
Receives simulated connected-vehicle telemetry and exposes it for retrieval.
Uses in-memory storage (see docs/threat-model.md and final-project-summary.md
for the limitations of this approach).
"""
from datetime import datetime, timezone
from typing import Dict

from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, Field

app = FastAPI(
    title="Telemetry Service",
    description="Receives and serves connected-vehicle telemetry data.",
    version="1.0.0",
)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# In-memory store: vehicle_id -> latest TelemetryEvent
_telemetry_store: Dict[str, "TelemetryEvent"] = {}


class TelemetryEvent(BaseModel):
    vehicle_id: str = Field(..., min_length=1, description="Vehicle identification number")
    speed: float = Field(..., ge=0, description="Speed in km/h")
    battery_level: float = Field(..., ge=0, le=100, description="Battery level percentage")
    temperature: float = Field(..., description="Battery/system temperature in Celsius")
    software_version: str = Field(..., min_length=1)
    timestamp: str | None = Field(
        default=None, description="ISO8601 timestamp; server time used if omitted"
    )


@app.get("/health")
def health():
    return {"status": "ok", "service": "telemetry-service"}


@app.post("/telemetry", status_code=201)
def post_telemetry(event: TelemetryEvent):
    if not event.vehicle_id.strip():
        raise HTTPException(status_code=422, detail="vehicle_id cannot be empty")

    if event.timestamp is None:
        event.timestamp = datetime.now(timezone.utc).isoformat()

    _telemetry_store[event.vehicle_id] = event
    return {"message": "telemetry recorded", "vehicle_id": event.vehicle_id}


@app.get("/telemetry/{vehicle_id}")
def get_telemetry(vehicle_id: str):
    event = _telemetry_store.get(vehicle_id)
    if event is None:
        raise HTTPException(status_code=404, detail="No telemetry found for this vehicle_id")
    return event
