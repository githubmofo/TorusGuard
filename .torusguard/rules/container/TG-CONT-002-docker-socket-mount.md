# TG-CONT-002: Dangerous Docker Socket Mount

## Severity
Critical. Mounting `/var/run/docker.sock` grants the container full root control over the host Docker daemon, enabling trivial container breakout and host root takeover.

## Applies To
- `docker-compose.yml`, `docker-compose.yaml`, `compose.yml`, `compose.yaml`
- Kubernetes PodSpecs, Helm charts, Docker run scripts

## Why It Matters
The Docker UNIX socket (`/var/run/docker.sock`) is the management API for the Docker daemon. Any process that can communicate with this socket can issue API calls to spawn new containers with host root filesystem mounts (`-v /:/host`), inspect all container secrets, and execute code directly on the host machine.

## What TorusGuard Looks For
1. Volume bindings referencing `/var/run/docker.sock:/var/run/docker.sock`.
2. Mounting the Docker socket in read-write or read-only mode without a hardening proxy.

## Unsafe Example
```yaml
# UNSAFE: Exposes host Docker daemon to the container
version: '3.8'
services:
  app:
    image: my-app:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

## Safe Example
```yaml
# SAFE: Remove Docker socket mount; use dedicated APIs or rootless sidecars
version: '3.8'
services:
  app:
    image: my-app:latest
    volumes:
      - app-data:/data
volumes:
  app-data:
```

## Remediation
1. Remove `/var/run/docker.sock` volume bindings from application containers.
2. If Docker commands are required, use unprivileged rootless container tooling (e.g., Kaniko for image builds) or a restricted Docker socket proxy that denies container-creation privileges.

## Related Rules
- `TG-CONT-001`: Root User Execution in Container
- `TG-CONT-003`: Privileged Container Mode
