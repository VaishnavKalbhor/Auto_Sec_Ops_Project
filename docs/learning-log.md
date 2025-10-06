# Learning Log

## Day 1

Today I defined the project scope. I decided to build a connected-vehicle backend with three services: telemetry, vehicle registry, and diagnostics.

The goal is not only to build APIs, but to show how DevSecOps practices can be added around automotive-style software delivery. Set up the repo structure (services/, tests/, docker/, k8s/, helm/, .github/workflows/, docs/, scripts/) and wrote the first pass of the README, architecture doc, and threat model.

## Day 2

Built the telemetry service: FastAPI app with in-memory storage, POST /telemetry, GET /telemetry/{vehicle_id}, /health, and /metrics via prometheus-fastapi-instrumentator. Wrote 5 pytest cases covering the happy path, validation, and 404 handling. Verified all tests pass locally before moving on.

## Day 3

Built the vehicle registry service: create/list/get vehicles, region validation (EU/US/APAC only), and duplicate vehicle_id rejection (409). 6 pytest cases, all passing.
