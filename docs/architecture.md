# Architecture

## Overview

AutoSecureOps consists of three independent FastAPI microservices simulating a connected-vehicle backend:

1. **Telemetry Service** — ingests live vehicle telemetry (speed, battery level, temperature, software version).
2. **Vehicle Registry Service** — stores vehicle metadata (model, owner type, region, software version).
3. **Diagnostics Service** — stores diagnostic trouble codes (DTCs) reported by vehicles.

Each service is independently deployable, independently tested, and independently containerized. They do not share a database; each currently uses in-memory storage, which is a documented limitation (see [threat-model.md](threat-model.md) and the final project summary).

## Data Flow

```
Vehicle (simulated)
   |
   |-- POST /vehicles ------------> Vehicle Registry Service
   |-- POST /telemetry ------------> Telemetry Service
   |-- POST /diagnostics ----------> Diagnostics Service
```

`scripts/generate_vehicle_events.py` simulates this flow end-to-end: register a vehicle, send telemetry, send a diagnostic code.

## Kubernetes Deployment

The system is deployed into a separate namespace. Each service has its own Deployment and Service. Health probes are used for availability checks, and basic securityContext settings are added to reduce container privileges.

## Local Development

All three services run together via `docker/docker-compose.yml` on ports 8001–8003.
