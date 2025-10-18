# DevSecOps Pipeline

## Pipeline Stages

1. Code checkout
2. Unit tests (per service, pytest)
3. Integration tests (cross-service vehicle flow)
4. SAST (Semgrep, CodeQL)
5. Dependency scanning (pip-audit)
6. Secret scanning (Gitleaks)
7. Docker image build
8. Container image scanning (Trivy)
9. DAST baseline scan (OWASP ZAP)
10. Kubernetes manifest / Helm chart validation

## Workflows

| Workflow | File | Purpose |
|---|---|---|
| CI | `.github/workflows/ci.yml` | Unit tests, integration tests, image builds |
| Security | `.github/workflows/security.yml` | Gitleaks, pip-audit, Semgrep |
| CodeQL | `.github/workflows/codeql.yml` | GitHub-native semantic code analysis |
| Container Scan | `.github/workflows/container-scan.yml` | Trivy vulnerability scan of built images |
| DAST | `.github/workflows/dast.yml` | OWASP ZAP baseline scan against a running service |
| Deploy (dev) | `.github/workflows/deploy-dev.yml` | Validates Kubernetes manifests and lints the Helm chart |

## Security Gate Policy

| Finding Type | Pipeline Result |
|---|---|
| Secret detected | Fail |
| Critical dependency vulnerability | Fail |
| Critical container vulnerability | Fail |
| High vulnerability | Warning + documented remediation |
| Medium/Low vulnerability | Report only |

Critical findings fail the pipeline. High findings are documented and reviewed
(see `docs/security-findings.md`). Medium and low findings are reported for
visibility but do not block a merge -- this keeps the pipeline useful rather
than something developers learn to ignore.
