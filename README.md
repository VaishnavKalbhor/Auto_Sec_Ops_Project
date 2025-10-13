# AutoSecureOps

A DevSecOps portfolio project for automotive-style connected vehicle services.

![CI](https://github.com/<your-github-username>/autosecureops/actions/workflows/ci.yml/badge.svg)


## Overview

AutoSecureOps is a connected-vehicle DevSecOps portfolio project. It simulates a small automotive backend where vehicles send telemetry and diagnostic data. The main purpose is to demonstrate secure CI/CD, automated testing, containerization, Kubernetes deployment, and security scanning.

## Why This Project

Modern automotive software is increasingly cloud-connected, continuously updated, and security-sensitive. This project demonstrates how DevSecOps practices can be applied to software delivery workflows in an automotive context.

## Learning Goals

- Build simple automotive-style microservices
- Add automated tests
- Containerize services with Docker
- Build CI/CD using GitHub Actions
- Add DevSecOps gates: SAST, dependency scan, secret scan, container scan
- Deploy to Kubernetes using Helm
- Add basic Kubernetes hardening with RBAC and NetworkPolicies
- Document findings like a real engineering project

## Services

| Service | Purpose |
|---|---|
| Telemetry Service | Receives vehicle telemetry |
| Vehicle Registry Service | Stores vehicle metadata |
| Diagnostics Service | Stores diagnostic fault codes |

## Architecture

See [docs/architecture.md](docs/architecture.md).

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

## Documentation

- [Architecture](docs/architecture.md)
- [Threat Model](docs/threat-model.md)
- [DevSecOps Pipeline](docs/devsecops-pipeline.md)
- [Security Findings](docs/security-findings.md)
- [Learning Log](docs/learning-log.md)
