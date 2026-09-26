# TG-CONT-004: Sensitive Credentials Passed via Container Build ARG or ENV

## Severity
High. Build arguments (`ARG`) and environment variables (`ENV`) declared in Dockerfiles persist in image metadata and history layers, leaking credentials to anyone with image read access.

## Applies To
- `Dockerfile`, `Dockerfile.*`, `Containerfile`
- Docker Compose build contexts

## Why It Matters
When a secret is passed via `ARG SECRET_KEY` or `ENV API_KEY=xyz` in a Dockerfile:
1. `docker history <image>` reveals the secret in clear text.
2. The credential is baked into intermediate layer metadata and pushed to container registries (Docker Hub, ECR, GCR).

## What TorusGuard Looks For
1. Dockerfile `ARG` or `ENV` directives declaring credentials matching `(?i)(password|secret|api_key|token|private_key)`.
2. Hardcoded secret assignments in `ENV` lines.

## Unsafe Example
```dockerfile
# UNSAFE: Bakes secret into image metadata
FROM python:3.11-slim
ARG GITHUB_TOKEN=ghp_9876543210fedcba
ENV DATABASE_PASSWORD=SuperSecretPass123!
```

## Safe Example
```dockerfile
# SAFE: Use BuildKit secrets mount or runtime environment injection
# syntax=docker/dockerfile:1.4
FROM python:3.11-slim
RUN --mount=type=secret,id=github_token \
    TOKEN=$(cat /run/secrets/github_token) && \
    pip install --extra-index-url https://$TOKEN@private.repo.com/packages
```

## Remediation
1. Use Docker BuildKit secret mounts (`RUN --mount=type=secret,id=mysecret`).
2. Pass runtime secrets via environment variable files at container run time, never build time.

## Related Rules
- `TG-SEC-001`: Hardcoded Secrets
- `TG-CONT-001`: Root User Execution in Container
