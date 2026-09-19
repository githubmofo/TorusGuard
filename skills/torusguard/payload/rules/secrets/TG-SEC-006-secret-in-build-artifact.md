# TG-SEC-006: Secret in Build Artifact or Container Image

## Severity
Critical. Copying `.env` files, build-time secrets, or SSH keys into Docker build layers persists secrets in image layers, allowing anyone with pull access to extract credentials via `docker history` or container inspection.

## Applies To
- Dockerfiles, Container Builds, Serverless Bundle Artifacts
- Docker, Containerd, Podman, Webpack, Vite

## Why It Matters
Docker image layers are cached and stored individually. Running `COPY .env .` followed by `RUN rm .env` still retains the `.env` file in the preceding layer blob, allowing trivial credential recovery.

## What TorusGuard Looks For
- Dockerfile instructions containing `COPY .env` or `ARG SECRET_KEY` without BuildKit secret mount protection.

## Unsafe Example
```dockerfile
# UNSAFE: Copying local .env into container layer
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY .env .
COPY . .
RUN npm run build
```

## Safe Example
```dockerfile
# SAFE: Using BuildKit secret mounts or multi-stage build without persisting secrets
# syntax=docker/dockerfile:1.4
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN --mount=type=secret,id=build_secrets npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
```

## Ponytail Remediation Budget
- Additions: <= 5 lines
- Deletions: <= 2 lines

## Remediation
1. Use Docker BuildKit secret mounts (`--mount=type=secret`) for credentials needed during build.
2. Use multi-stage Docker builds to ensure final runtime images only contain compiled frontend assets.

## Related Rules
- `TG-SUPPLY-006`: Container Build Secret Persistence
- `TG-SEC-001`: Hardcoded Secret or API Key in Tracked Source
