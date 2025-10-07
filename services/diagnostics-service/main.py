"""
Diagnostics Service
Receives diagnostic trouble codes (DTCs) reported by connected vehicles.
Uses in-memory storage (see docs/threat-model.md for limitations).
"""
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="Diagnostics Service",
    description="Receives and serves vehicle diagnostic trouble codes.",
    version="1.0.0",
)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

ALLOWED_SEVERITIES = {"low", "medium", "high", "critical"}

# In-memory store: vehicle_id -> list of DiagnosticEvent
_diagnostics_store: Dict[str, List["DiagnosticEvent"]] = {}


class DiagnosticEvent(BaseModel):
    vehicle_id: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1, description="Diagnostic trouble code, e.g. P0562")
    severity: str
    description: str = Field(..., min_length=1)

    @field_validator("severity")
    @classmethod
    def severity_must_be_valid(cls, v: str) -> str:
        if v not in ALLOWED_SEVERITIES:
            raise ValueError(f"severity must be one of {sorted(ALLOWED_SEVERITIES)}")
        return v


@app.get("/health")
def health():
    return {"status": "ok", "service": "diagnostics-service"}


@app.post("/diagnostics", status_code=201)
def post_diagnostic(event: DiagnosticEvent):
    _diagnostics_store.setdefault(event.vehicle_id, []).append(event)
    return event


@app.get("/diagnostics/{vehicle_id}", response_model=List[DiagnosticEvent])
def get_diagnostics(vehicle_id: str):
    events = _diagnostics_store.get(vehicle_id)
    if events is None:
        raise HTTPException(status_code=404, detail="No diagnostics found for this vehicle_id")
    return events
