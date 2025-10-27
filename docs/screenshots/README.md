# Screenshots

This folder is for evidence screenshots referenced in the main README and
docs/final-project-summary.md. Capture these once the pipeline has actually
run on GitHub / against a real cluster -- don't fabricate them:

- github-actions-ci.png -- a green run of `.github/workflows/ci.yml`
- github-actions-security.png -- a run of `.github/workflows/security.yml`
- trivy-scan.png -- Trivy output/summary from container-scan.yml
- zap-report.png -- the OWASP ZAP baseline report artifact
- docker-compose-running.png -- `docker compose up --build` with all 3
  services healthy
- kubernetes-pods.png -- `kubectl get pods -n autosecureops` showing
  running pods
- api-docs-swagger.png -- one service's `/docs` (FastAPI's auto-generated
  Swagger UI)
