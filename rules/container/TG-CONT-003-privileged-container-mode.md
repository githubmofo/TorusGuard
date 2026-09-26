# TG-CONT-003: Privileged Container Mode or Disabled Security Profile

## Severity
Critical. Running in privileged mode disables all Linux security protections, capabilities restrictions, and seccomp filters, granting the container full raw device and kernel access.

## Applies To
- `docker-compose.yml`, `docker-compose.yaml`, `compose.yml`
- Kubernetes PodSpecs (`securityContext.privileged: true`)
- Docker CLI arguments (`--privileged`)

## Why It Matters
The `--privileged` flag gives all capabilities to the container and lifts all limitations enforced by the device cgroup controller. A privileged container can access host device nodes (`/dev`), load kernel modules, and escape into the host operating system with minimal effort.

## What TorusGuard Looks For
1. `privileged: true` in Compose files.
2. `security_opt: ["seccomp:unconfined"]` or `security_opt: ["apparmor:unconfined"]`.
3. `cap_add: ["ALL"]` or `cap_add: ["SYS_ADMIN"]`.

## Unsafe Example
```yaml
# UNSAFE: Full privileged access and unconfined seccomp
version: '3.8'
services:
  web:
    image: web:latest
    privileged: true
    security_opt:
      - seccomp:unconfined
```

## Safe Example
```yaml
# SAFE: Unprivileged execution with dropped capabilities
version: '3.8'
services:
  web:
    image: web:latest
    privileged: false
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    read_only: true
```

## Remediation
1. Set `privileged: false` (or remove the attribute).
2. Explicitly drop all capabilities (`cap_drop: ["ALL"]`) and add only specific minimal capabilities (e.g. `NET_BIND_SERVICE`).
3. Enable default seccomp profiles.

## Related Rules
- `TG-CONT-001`: Root User Execution in Container
- `TG-CONT-002`: Dangerous Docker Socket Mount
