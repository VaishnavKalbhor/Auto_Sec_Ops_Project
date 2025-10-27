# AutoSecureOps

A DevSecOps portfolio project for automotive-style connected vehicle services.

![CI](https://github.com/<your-github-username>/autosecureops/actions/workflows/ci.yml/badge.svg)

## Overview

AutoSecureOps simulates a cloud backend for connected vehicles. It includes
telemetry ingestion, vehicle registration, and diagnostics APIs. Around
these services, the project implements a secure CI/CD pipeline with
automated testing, static analysis, dependency scanning, secret scanning,
container scanning, Kubernetes deployment, and basic runtime hardening.

## Why This Project

Modern automotive software is increasingly cloud-connected, continuously
updated, and security-sensitive. This project demonstrates how DevSecOps
practices can be applied to software delivery workflows in an automotive
context.

## Architecture

See [docs/architecture.md](docs/architecture.md) for the full breakdown.

```
Vehicle (simulated)
   |
   |-- POST /vehicles ------------> Vehicle Registry Service
   |-- POST /telemetry ------------> Telemetry Service
   |-- POST /diagnostics ----------> Diagnostics Service
```

## Services

| Service | Purpose |
|---|---|
| Telemetry Service | Receives vehicle telemetry |
| Vehicle Registry Service | Stores vehicle metadata |
| Diagnostics Service | Stores diagnostic fault codes |

## DevSecOps Features

| Area | Tool |
|---|---|
| CI/CD | GitHub Actions |
| Unit Testing | Pytest |
| SAST | Semgrep, CodeQL |
| SCA | pip-audit |
| Secret Scanning | Gitleaks |
| Container Scanning | Trivy |
| DAST | OWASP ZAP |
| Kubernetes | Manifests + Helm |
| Hardening | RBAC, NetworkPolicy, securityContext |
| Observability | Prometheus metrics |

## Getting Started

```bash
cd docker
docker compose up --build
```

Then:

```bash
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
```

Simulate a full vehicle flow (register -> telemetry -> diagnostic) against
the running services:

```bash
pip install httpx
python scripts/generate_vehicle_events.py
```

Run the test suites:

```bash
pip install -r services/telemetry-service/requirements.txt
pip install -r services/vehicle-registry-service/requirements.txt
pip install -r services/diagnostics-service/requirements.txt
pytest services/telemetry-service -v
pytest services/vehicle-registry-service -v
pytest services/diagnostics-service -v
pytest tests/integration tests/security -v
```

## Documentation

- [Architecture](docs/architecture.md)
- [Threat Model](docs/threat-model.md)
- [DevSecOps Pipeline](docs/devsecops-pipeline.md)
- [Security Findings](docs/security-findings.md)
- [Observability](docs/observability.md)
- [Learning Log](docs/learning-log.md)
- [Final Project Summary](docs/final-project-summary.md)

## Screenshots

See [docs/screenshots/README.md](docs/screenshots/README.md) for the list of
evidence screenshots this project references (CI runs, security scans,
Docker Compose, Kubernetes pods, Swagger UI).

## Learning Outcomes

This project helped me understand how DevSecOps is implemented as a
pipeline of checks and controls rather than a single tool. See
[docs/final-project-summary.md](docs/final-project-summary.md) for the full
writeup, including known limitations.
