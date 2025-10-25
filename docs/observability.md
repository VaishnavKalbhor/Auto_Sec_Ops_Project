# Observability

## Metrics

Each service exposes a `/metrics` endpoint (via `prometheus-fastapi-instrumentator`).
The goal is to make service health, request count, latency, and error rate
visible to a monitoring system such as Prometheus.

| Service | Metrics endpoint |
|---|---|
| Telemetry | `http://localhost:8001/metrics` |
| Vehicle Registry | `http://localhost:8002/metrics` |
| Diagnostics | `http://localhost:8003/metrics` |

Default metrics include request counts by path/method/status, request
duration histograms, and in-progress request gauges -- enough to build basic
Grafana panels (request rate, error rate, p95 latency) per service.

## GitOps (ArgoCD)

`argocd/application.yaml` defines an ArgoCD Application pointing at
`helm/autosecureops`, with automated sync, self-heal, and namespace creation
enabled. This is written and ready to apply against a cluster with ArgoCD
installed (`kubectl apply -f argocd/application.yaml`), but has not been
exercised against a live ArgoCD instance as part of this build -- there's no
cluster available in this sandbox. Treat it as a documented starting point,
not a verified deployment path, until it's been run for real.

## Optional local stack

A Prometheus + Grafana pair added to `docker/docker-compose.yml` (scraping
each service's `/metrics`) would complete the local observability picture.
Not included by default to keep the base compose file focused, but noted
here as a natural next step.
