# Final Project Summary

## Project Goal

This project simulates a connected-vehicle backend and demonstrates how
DevSecOps practices can be applied to automotive-style cloud services.

## What I Built

- Telemetry service
- Vehicle registry service
- Diagnostics service
- Dockerized local environment (docker-compose)
- GitHub Actions CI pipeline (unit tests, integration tests, image builds)
- Security scanning pipeline (Semgrep, CodeQL, Gitleaks, pip-audit, Trivy, ZAP)
- Kubernetes manifests
- Helm chart
- NetworkPolicies and basic RBAC
- Security findings documentation
- Basic load test and vehicle-flow simulator

## DevSecOps Controls Implemented

| Control | Tool |
|---|---|
| Unit tests | Pytest |
| CI/CD | GitHub Actions |
| SAST | Semgrep / CodeQL |
| Dependency scanning | pip-audit |
| Secret scanning | Gitleaks |
| Container scanning | Trivy |
| DAST | OWASP ZAP baseline |
| Kubernetes hardening | securityContext, RBAC, NetworkPolicy |
| Observability | Prometheus metrics |

## What I Learned

- How to structure a microservice project for CI/CD from day one, rather
  than bolting it on afterward.
- The practical difference between SAST, SCA, container scanning and DAST --
  each catches a different class of issue at a different stage of the
  pipeline.
- How security gates can fail a pipeline before deployment, and why a
  gate policy (critical fails, high warns, medium/low reports) matters more
  than trying to block on every finding.
- How Kubernetes security settings (securityContext, RBAC, NetworkPolicy)
  reduce runtime blast radius even for a small system.
- That DevSecOps is not one tool, but a chain of small controls across the
  software lifecycle -- and that documenting *why* a control exists is as
  important as adding it.

## Limitations

- Services use in-memory storage; nothing survives a restart.
- Authentication is not implemented (no auth on any endpoint).
- Kubernetes manifests and the Helm chart were written and YAML-validated,
  but not run against a real cluster in this build (no kind/minikube/Docker
  available in the sandbox this project was scaffolded in) -- validate with
  `kubectl apply --dry-run` / `helm lint` / `helm template` before treating
  them as verified, and take the kubernetes-pods.png screenshot once that's
  done.
- Docker Compose was written and reviewed but not run in this environment
  either (no Docker daemon available here) -- run `docker compose up --build`
  once on a machine with Docker before considering that step verified.
- Security tools (Semgrep, ZAP) are wired into CI but their actual detection
  was not confirmed locally (semgrep failed to install in time in this
  sandbox) -- confirm on the first real GitHub Actions run.
- The project is a simulation, not a real vehicle system.
- Security gates are simplified for learning purposes.

## Future Improvements

- Add PostgreSQL (replace in-memory storage)
- Add OAuth2/JWT authentication
- Add SBOM generation with CycloneDX or Syft
- Add policy-as-code with OPA/Conftest
- Add full GitOps deployment with ArgoCD (manifest is ready, unexercised)
- Add centralized logging with Loki
- Add Prometheus + Grafana to docker-compose for local observability
