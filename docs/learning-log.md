# Learning Log

## Day 1

Today I defined the project scope. I decided to build a connected-vehicle backend with three services: telemetry, vehicle registry, and diagnostics.

The goal is not only to build APIs, but to show how DevSecOps practices can be added around automotive-style software delivery. Set up the repo structure (services/, tests/, docker/, k8s/, helm/, .github/workflows/, docs/, scripts/) and wrote the first pass of the README, architecture doc, and threat model.

## Day 2

Built the telemetry service: FastAPI app with in-memory storage, POST /telemetry, GET /telemetry/{vehicle_id}, /health, and /metrics via prometheus-fastapi-instrumentator. Wrote 5 pytest cases covering the happy path, validation, and 404 handling. Verified all tests pass locally before moving on.

## Day 3

Built the vehicle registry service: create/list/get vehicles, region validation (EU/US/APAC only), and duplicate vehicle_id rejection (409). 6 pytest cases, all passing.

## Day 4

Built the diagnostics service: accepts DTC codes with severity validation (low/medium/high/critical), returns list of codes per vehicle. 5 pytest cases, all passing. All three services now exist and their test suites pass locally (16 tests total).

## Day 5

Wrote Dockerfiles for all three services (python:3.12-slim base, non-root-friendly, HEALTHCHECK hitting /health) and docker/docker-compose.yml wiring them up on ports 8001-8003. This step is meant to be run with Docker Desktop/Engine on a dev machine; the sandbox this project was scaffolded in doesn't have a Docker daemon, so this was verified by structural review rather than an actual `docker compose up` run -- worth double-checking locally before treating it as done.

## Day 6

Added scripts/generate_vehicle_events.py to simulate a full vehicle flow (register -> telemetry -> diagnostic) against live services, and tests/integration/test_vehicle_flow.py which drives the same flow in-process across all three FastAPI apps. This isn't real service-to-service networking yet -- each service is still independent with no shared database -- but it proves the automotive data flow works end-to-end. 4/4 integration tests passing.

## Day 7

Added .github/workflows/ci.yml: a matrix job running pytest for each of the three services, a separate job running the cross-service integration tests, and a job building each service's Docker image. Added a CI badge placeholder to the README (needs the real GitHub username once the repo is pushed).

## Day 8

Added .github/workflows/security.yml with three jobs: Gitleaks secret scanning, pip-audit dependency scanning per service, and Semgrep SAST (security-audit + python rulesets). Added tests/security/insecure_demo.py with an intentionally vulnerable subprocess(shell=True) pattern plus the fixed version, and documented the finding in docs/security-findings.md. Tried to install semgrep locally to confirm detection before pushing, but the install didn't finish in this sandbox (large package, slow network) -- this needs a real run in GitHub Actions (or a local machine with a faster connection) to confirm the rule actually fires before relying on it.
