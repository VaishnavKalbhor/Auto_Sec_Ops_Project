"""
Vehicle Registry Service
Stores basic vehicle metadata (model, owner type, region, software version).
Uses in-memory storage (see docs/threat-model.md for limitations).
"""
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="Vehicle Registry Service",
    description="Stores connected-vehicle metadata.",
    version="1.0.0",
)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

ALLOWED_REGIONS = {"EU", "US", "APAC"}

# In-memory store: vehicle_id -> Vehicle
_registry: Dict[str, "Vehicle"] = {}


class Vehicle(BaseModel):
    vehicle_id: str = Field(..., min_length=1)
    model: str = Field(..., min_length=1)
    owner_type: str = Field(..., min_length=1)
    region: str
    software_version: str = Field(..., min_length=1)

    @field_validator("vehicle_id")
    @classmethod
    def vehicle_id_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("vehicle_id cannot be empty")
        return v

    @field_validator("region")
    @classmethod
    def region_must_be_valid(cls, v: str) -> str:
        if v not in ALLOWED_REGIONS:
            raise ValueError(f"region must be one of {sorted(ALLOWED_REGIONS)}")
        return v


@app.get("/health")
def health():
    return {"status": "ok", "service": "vehicle-registry-service"}


@app.post("/vehicles", status_code=201)
def create_vehicle(vehicle: Vehicle):
    if vehicle.vehicle_id in _registry:
        raise HTTPException(status_code=409, detail="vehicle_id already registered")
    _registry[vehicle.vehicle_id] = vehicle
    return vehicle


@app.get("/vehicles", response_model=List[Vehicle])
def list_vehicles():
    return list(_registry.values())


@app.get("/vehicles/{vehicle_id}", response_model=Vehicle)
def get_vehicle(vehicle_id: str):
    vehicle = _registry.get(vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle
