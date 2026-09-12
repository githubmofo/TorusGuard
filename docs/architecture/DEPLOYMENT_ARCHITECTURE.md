# TorusGuard Deployment & Runtime Architecture

## 1. Overview
TorusGuard is engineered with a **zero-daemon, local-first architecture**. It operates seamlessly within developer workstations, containerized CI/CD pipelines, and multi-agent IDE runtimes without requiring external background daemons, network ports, or SaaS backends.

---

## 2. Supported Deployment Topologies

```text
                               ┌────────────────────────────────┐
                               │  TorusGuard Core Distribution  │
                               └───────────────┬────────────────┘
                                               │
             ┌─────────────────────────────────┼─────────────────────────────────┐
             ▼                                 ▼                                 ▼
┌─────────────────────────┐       ┌─────────────────────────┐       ┌─────────────────────────┐
│   AI Agent IDE Runtime  │       │   CI/CD Automated Gate  │       │  Air-Gapped Workstation │
│ (Cursor, Claude Code,   │       │ (GitHub Actions, GitLab,│       │ (Local Enterprise Repo, │
│  Antigravity, Windsurf) │       │  Jenkins Pipeline)      │       │  Zero External Network) │
└─────────────────────────┘       └─────────────────────────┘       └─────────────────────────┘
```

### 2.1. Topology A: Terminal CLI & AI Agent Workspace Integration
- **Mechanism:** Installed via standard NPM package (`npm install -g torusguard` or run via `npx torusguard <cmd>`).
- **Autonomous Bootstrapping:** Automatically creates `.torusguard/`, activates 74 rules across 18 families, and synchronizes rules into `.cursorrules`, `CLAUDE.md`, and `.windsurfrules`.
- **Triggering:** Dual invocation via terminal CLI (`npx torusguard audit`) and chat slash commands (`/torusguard audit`).
- **Local Pre-Commit Hook:** Installed via `npx torusguard diff-guard --install-hook` to intercept security bypasses before `git commit`.

### 2.2. Topology B: CI/CD Pipeline Enforcement
- **Mechanism:** Executed as a zero-dependency automated gate in CI/CD runners.
- **Living Report Ground Truth:** Audit runs maintain `security_report.md` at repository root, preventing regressions and tracking health score (0–100).
- **Example GitHub Actions Workflow:**
```yaml
name: TorusGuard Security Gate
on: [push, pull_request]

jobs:
  security-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Node & Python
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Run Core Test Harnesses
        run: npm test
      - name: Run Static Security Audit
        run: npx torusguard audit
      - name: Generate Visual HTML Report
        run: npx torusguard report --html
      - name: Upload SARIF Security Results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: .torusguard/runs/results.sarif
          category: torusguard/static
```

### 2.3. Topology C: Air-Gapped / High-Security Environments
- **Zero Egress Guarantee:** TorusGuard contains zero analytics, tracking, or outbound HTTP requests.
- **Offline Operation:** All 74 rules, schemas, and verification logic are bundled locally within the repository with 0-byte external network footprint.

---

## 3. Resource Requirements & Operational Footprint
- **CPU:** 1 vCPU (sub-second execution on standard codebases).
- **RAM:** $< 150\text{ MB}$ base memory usage.
- **Disk:** $< 20\text{ MB}$ installation footprint + $< 2\text{ MB}$ per audit run folder.
- **OS Compatibility:** Linux (Ubuntu/Debian, Alpine, RHEL), macOS (Apple Silicon & Intel), Windows (PowerShell/CMD).
- **Zero External Python Dependencies:** Pure standard library execution (Python 3.10+).
