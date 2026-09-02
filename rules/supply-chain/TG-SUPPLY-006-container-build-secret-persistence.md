# TG-SUPPLY-006: Container Build Secret Persistence

## Severity
High. Embedding credentials, tokens, or private SSH keys into intermediate container build layers exposes secrets in public registry images.

## Applies To
- Dockerfiles, Containerfile, Docker Compose
- CI/CD Container Build Pipelines

## Why It Matters
When `ARG`, `ENV`, or `COPY` directives are used to pass secrets into Docker builds:
1. Every Docker layer is cached and preserved in the final image manifest.
2. Even if a subsequent `RUN rm -rf /root/.ssh` is executed, the file remains fully recoverable using container layer extractors (`dive`, `docker history`).
3. Deploying the image to public or shared registries inadvertently leaks production credentials.

## What TorusGuard Looks For
1. `ARG` or `ENV` variables with names matching `TOKEN`, `KEY`, `PASSWORD`, `SECRET`.
2. Direct `COPY` of private SSH keys (`id_rsa`), `.env` files, or npm tokens (`.npmrc`) into build images.
3. Multi-stage builds copying secret artifacts from builder stages without BuildKit secret mounts.

## Unsafe Example
```dockerfile
# UNSAFE: Passing GitHub token via build-arg leaves it in layer metadata
FROM node:20-alpine
ARG GITHUB_TOKEN
ENV GITHUB_TOKEN=$GITHUB_TOKEN

# Secrets remain in image history forever!
RUN npm install
```

## Safe Example
```dockerfile
# SAFE: Using BuildKit secret mounts (never persisted to image layers)
# syntax=docker/dockerfile:1.4
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./

# Secret is mounted ephemerally in RAM during the command and never written to disk
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci --only=production

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .

USER node
CMD ["node", "server.js"]
```

## Remediation
1. **Use BuildKit Secret Mounts:** Replace `ARG` secrets with `RUN --mount=type=secret,id=my_secret`.
2. **Multi-Stage Clean Separation:** Compile code in an unprivileged builder stage and copy strictly compiled runtime artifacts to the runner image.
3. **Use `.dockerignore`:** Exclude `.env`, `.git`, `.npmrc`, and credentials from build context.

## Related Rules
- `TG-SEC-001`: Hardcoded Secrets
- `TG-SUPPLY-002`: Vulnerable Dependency Review Missing
