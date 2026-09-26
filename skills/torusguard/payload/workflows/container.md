# /torusguard-container — Container & Docker Security Audit

$ARGUMENTS

---

## Objective
Detect and remediate container privilege escalation, root execution, docker socket exposure, and build-time secret injection across `Dockerfile`, `Containerfile`, and `docker-compose.yml` configurations.

---

## Tri-Mode Parity
- **Mode A (Terminal CLI):** `torusguard container [target]`
- **Mode B (AI Chat Slash Command):** `/torusguard container [target]`
- **Mode C (Native MCP Tool):** `torusguard_container`

---

## Execution Steps

1. **Discover Container Configurations:** Discover all Dockerfiles and compose YAML files in the workspace.
2. **Execute Static Heuristic Audit:** Run `ScanContainerFiles` or `torusguard_container` against discovered files.
3. **Assert Security Invariants:**
   - Enforce non-root user declarations (`TG-CONT-001`).
   - Block Docker daemon socket mounts (`/var/run/docker.sock`) (`TG-CONT-002`).
   - Disallow `privileged: true` and unconfined seccomp profiles (`TG-CONT-003`).
   - Ban build-time secrets in `ARG` or `ENV` directives (`TG-CONT-004`).
4. **Formulate Surgical Patches:** Propose minimal diffs adding non-root users (`USER appuser`) and secret mounts within Ponytail bounds (≤35 additions, ≤25 deletions).
5. **Synchronize Report:** Log all container findings in `security_report.md`.
