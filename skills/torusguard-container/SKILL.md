---
name: torusguard-container
description: Audits Dockerfiles, Containerfiles, and Docker Compose configurations for root users, exposed docker sockets, privileged mode, and embedded secrets via CLI, Chat, or MCP.
version: 2.0.0
workflow: .torusguard/workflows/container.md
tools: Read, Grep, Glob, Write, run_command
scripts-binding:
  - internal/scanner/container.go
  - cmd/torusguard/main.go
  - cmd/torusguard/mcp.go
---

# TorusGuard Container & Docker Security Audit

## Objective
Detect and remediate critical container runtime and build-time security vulnerabilities across `Dockerfile`, `Containerfile`, `docker-compose.yml`, and `compose.yaml` files. Enforces non-root execution, privilege containment, socket isolation, and BuildKit secret mounts.

---

## Tri-Mode Execution

### Mode A: Automated CLI Execution
Run container audits against current directory or specific target project:
```bash
# Scan container files in current directory
torusguard container

# Scan container files in specific workspace target
torusguard container --target ./deployments/docker
```

### Mode B: In-Session AI Chat Slash Command
Run `/torusguard container` in chat.
The agent invokes the native Go scanner or MCP tool to inspect container definitions, audit user permissions, and report structural container misconfigurations.

### Mode C: Native MCP Tool Call
MCP-enabled coding agents (Antigravity, Cursor, Windsurf, Claude Code) call:
```json
{
  "tool": "torusguard_container",
  "arguments": {
    "target": "."
  }
}
```

---

## Supported Patterns & Invariants
- **TG-CONT-001 (Root Execution Default):** Detects omission of explicit `USER <non-root>` instruction or explicit `USER root` declarations in production container stages.
- **TG-CONT-002 (Docker Socket Exposure):** Detects dangerous mounting of the host daemon socket (`/var/run/docker.sock`), which grants unconfined root privileges over the host.
- **TG-CONT-003 (Privileged Container Flag):** Detects `privileged: true`, `seccomp:unconfined`, or `SYS_ADMIN` capability grants that defeat Linux namespace and cgroup boundaries.
- **TG-CONT-004 (Build-Time Secret Injection):** Flags embedding sensitive tokens, passwords, or keys via `ARG` or `ENV` directives in Dockerfiles rather than BuildKit secret mounts.

---

## 🏛️ OpenCodeReview Hybrid Architecture Integration
- **Deterministic Dockerfile & Compose Parser:** Pattern extraction is executed by Go AST/regex parsers without external Docker daemon dependencies.
- **Token Efficiency:** Only flagged container directives and minimal surrounding context are returned to the agent context.
- **Ponytail Bounds:** Remediation patches must add dedicated non-root users (`USER appuser`) or switch secrets to `--mount=type=secret` without full container file rewrites (≤35 additions, ≤25 deletions).

---

## 🚨 LLM Trap Table

| Pattern | What AI Does Wrong | What Is Actually Correct |
| :--- | :--- | :--- |
| **Default Root Execution** | Forgets that Docker executes as UID 0 (`root`) unless a non-root `USER` is declared. | Always declare `RUN adduser -D appuser && USER appuser` before the entrypoint. |
| **Secrets in Build Arguments** | Recommends `ARG API_KEY` or `ENV DB_PASSWORD`, leaving keys baked into image layers. | Use Docker BuildKit secret mounts: `RUN --mount=type=secret,id=mysecret ...`. |
| **Permissive Privileged Mode** | Adds `privileged: true` or `cap_add: [ALL]` to resolve permission or port binding errors. | Grant only specific minimal Linux capabilities (e.g. `NET_BIND_SERVICE`) or fix file ownership. |
| **Docker Socket Mounting** | Mounts `/var/run/docker.sock` inside container to run Docker commands inside Docker. | Use Docker-in-Docker (dind) rootless or ephemeral CI runners with isolated daemons. |
| **Full File Rewrites** | Rewrites entire multi-stage Dockerfile destroying cached layer order. | Formulate surgical diffs replacing or inserting only the missing `USER` or mount flag. |

---

## ✅ Pre-Flight Self-Audit

Before concluding a container security review, verify:
- [ ] Did I scan all Dockerfiles (`Dockerfile`, `Dockerfile.*`, `Containerfile`)?
- [ ] Did I scan all compose files (`docker-compose.yml`, `compose.yaml`)?
- [ ] Is there an unprivileged non-root user defined before `ENTRYPOINT` or `CMD`?
- [ ] Are sensitive environment variables passed via runtime `.env` / secret managers instead of `ARG` / `ENV`?
- [ ] Is `/var/run/docker.sock` completely absent from compose volumes?
- [ ] Are all proposed fixes within Ponytail churn bounds (≤35 additions, ≤25 deletions)?

---

## 🔁 VBC Protocol (Verify → Build → Confirm)

```
VERIFY: Identify Dockerfiles and Compose files in the workspace.
BUILD:  Execute torusguard container or torusguard_container to locate container privilege and secret flaws.
CONFIRM: Formulate surgical remediation patch introducing non-root users and removing dangerous mounts, rechecking with torusguard recheck.
```
