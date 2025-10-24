# autosecureops Helm chart

Deploys the three AutoSecureOps microservices (telemetry, vehicle registry,
diagnostics) into a single namespace.

## Usage

```bash
helm install autosecureops ./helm/autosecureops
```

## Values

| Key | Description | Default |
|---|---|---|
| `namespace` | Target namespace | `autosecureops` |
| `image.repository` | Image repo prefix | `autosecureops` |
| `image.tag` | Image tag | `latest` |
| `replicaCount` | Replicas per service | `2` |
| `service.port` | Service port | `80` |
| `service.targetPort` | Container port | `8000` |
| `resources` | CPU/memory requests+limits | see values.yaml |
| `services` | List of services to deploy | see values.yaml |
