# TG-CONT-001: Root User Execution in Container

## Severity
High. Running container processes as root increases the blast radius of any remote code execution (RCE) flaw, enabling container breakout and host compromise.

## Applies To
- `Dockerfile`, `Dockerfile.*`, `Containerfile`
- Docker Compose (`docker-compose.yml`, `compose.yaml`)
- Kubernetes PodSpecs

## Why It Matters
By default, Docker executes container entrypoints as the `root` user (UID 0). If an application vulnerability (e.g., path traversal, command injection, or memory corruption) is exploited, the attacker immediately possesses root privileges within the container, facilitating kernel exploits, namespace escapes, and host file access.

## What TorusGuard Looks For
1. Dockerfiles lacking an explicit non-root `USER <user>` directive.
2. Explicit `USER root` or `USER 0` declarations without dropping privileges.
3. Compose services declaring `user: "0"` or `user: "root"`.

## Unsafe Example
```dockerfile
# UNSAFE: No USER declared; runs as root
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "server.js"]
```

## Safe Example
```dockerfile
# SAFE: Dedicated unprivileged non-root user
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
CMD ["node", "server.js"]
```

## Remediation
1. Declare a non-privileged user and group (`USER appuser` or `USER 10001:10001`).
2. Ensure file permissions allow the non-root user to read necessary application files.
3. In Compose files, set `user: "10001:10001"`.

## Related Rules
- `TG-CONT-002`: Dangerous Docker Socket Mount
- `TG-CONT-003`: Privileged Container Mode
