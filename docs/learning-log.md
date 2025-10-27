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

## Day 9

Added .github/workflows/codeql.yml (GitHub-native SAST, weekly scheduled scan plus PR/push triggers) and container-scan.yml (Trivy against each service's built image, following the documented gate policy: report HIGH+CRITICAL, only fail the pipeline on CRITICAL). Also added deploy-dev.yml as a manual workflow_dispatch job that dry-run validates the Kubernetes manifests and lints the Helm chart (both added on Day 11-12) before any real deploy step is wired up. Wrote docs/devsecops-pipeline.md tying all the workflows together with the gate policy table.

## Day 10

Added .github/workflows/dast.yml running an OWASP ZAP baseline scan against the telemetry-service (started in-workflow, scanned, report uploaded as an artifact; SAST covers source code, DAST covers the running app from the outside). Also added tests/security/test_basic_api_security.py -- parametrized across all three services -- checking that /health doesn't leak secrets, unknown routes 404, and malformed payloads never return a raw 500. 12/12 passing locally.

## Day 11

Added Kubernetes base manifests: a dedicated `autosecureops` namespace, and a Deployment + Service per microservice (2 replicas each) with readiness/liveness probes on /health, resource requests/limits, and a securityContext (runAsNonRoot, no privilege escalation, all capabilities dropped). Validated all 7 YAML files parse correctly with PyYAML -- I don't have a real cluster (kind/minikube) in this sandbox to `kubectl apply` against, so that's still untested against an actual API server and worth a real dry-run before relying on it.

## Day 12

Hand-wrote the Helm chart (helm binary isn't available in this sandbox, so I built Chart.yaml/values.yaml/templates directly rather than running `helm create`) -- values.yaml drives image repo/tag, replica count, service ports, resources, and a per-service env list, with deployment/service templates ranging over `.Values.services`. Added NetworkPolicies: default-deny-ingress as the baseline, then explicit allows for service-to-service traffic on 8000 and for a `monitoring` namespace to scrape /metrics. Added a minimal ServiceAccount + Role (get/list on pods and configmaps only) + RoleBinding under k8s/base, referenced by both the raw manifests and the Helm templates. All plain-YAML files validated with PyYAML; the Helm templates use Go templating so they weren't rendered/validated here (no helm binary) -- worth a `helm template` / `helm lint` pass locally before treating the chart as verified.

## Day 13

Added argocd/application.yaml (GitOps: points at the Helm chart, automated sync + self-heal + CreateNamespace) and docs/observability.md documenting the /metrics endpoints already present on all three services since Day 2-4 (prometheus-fastapi-instrumentator) and what a Prometheus/Grafana addition to docker-compose would look like. Confirmed all three services already expose /metrics (checked main.py for each) -- no code changes needed here, just documentation. ArgoCD manifest is unverified against a real cluster; noted as such in the doc rather than claiming it works.

## Day 14

Final polish pass. Added tests/load/basic_load_test.py and actually ran it against a live telemetry-service instance (300/300 succeeded, ~1.3ms average) rather than just writing it and hoping. Added docs/final-project-summary.md (goals, controls table, honest limitations, future work) and docs/screenshots/README.md listing exactly which screenshots still need to be captured against a real run. Rewrote README.md into the full structure (overview, why, architecture, services table, DevSecOps features table, getting started, docs links, screenshots, learning outcomes).

Also caught and fixed a real bug during a full-repo verification pass: running `pytest` across all three services from the repo root failed, first with a `tests` package name collision (all three services + top-level tests/integration share the package name "tests"), then -- after fixing that with a root pytest.ini (`--import-mode=importlib`) -- with a second, subtler bug where all three services' test files did `from main import app`, so Python's module cache reused whichever service's `main.py` loaded first for all three, silently testing the wrong app in two of them. Fixed by giving each service's test file a uniquely-named module import (matching the pattern already used in tests/integration and tests/security). Full suite: 32/32 passing from repo root.

## Known gaps going into review

Documented in docs/final-project-summary.md, but worth repeating here since it's the honest state of things: Docker Compose, the Kubernetes manifests, the Helm chart, and the security scanners (Semgrep/Gitleaks/Trivy/ZAP/CodeQL) were all written carefully and validated where a local check was possible (YAML syntax, pytest), but none of them have been run for real in this sandbox (no Docker daemon, no cluster, no helm binary, and semgrep's install didn't finish over this connection). The first real GitHub Actions run and the first real `docker compose up` / `kubectl apply` / `helm lint` are the actual verification of those pieces -- treat this build as "ready to verify," not "verified."
