# Threat Model

## Assets

- Vehicle telemetry data
- Vehicle identity data
- Diagnostic fault data
- API endpoints
- Container images
- CI/CD pipeline
- Kubernetes cluster

## Threats

| Threat | Example | Mitigation |
|---|---|---|
| Secret leakage | API key committed to Git | Gitleaks |
| Vulnerable dependency | Outdated Python package | Dependency scan (pip-audit) |
| Insecure container image | Critical CVE in base image | Trivy |
| API abuse | Invalid payloads or fuzzing | Validation and error handling |
| Lateral movement | One pod talks to all pods | NetworkPolicy |
| Excessive permissions | Service has broad cluster access | RBAC |
| Insecure code pattern | Shell injection | Semgrep / CodeQL |

## Limitations

This is a learning project and does not represent a production-grade automotive cybersecurity system. Services use in-memory storage, authentication is minimal, and Kubernetes deployment is tested locally rather than in a production cluster.
