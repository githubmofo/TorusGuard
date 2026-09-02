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
│  Antigravity, Cline)    │       │  Jenkins Pipeline)      │       │  Zero External Network) │
└─────────────────────────┘       └─────────────────────────┘       └─────────────────────────┘
```

### 2.1. Topology A: AI Agent Skill & Workspace Integration
- **Mechanism:** Installed via standard skill package managers (`npx skills add ...`) or direct Python installer (`python install.py`).
- **Autonomous Bootstrapping:** Automatically creates `.torusguard/`, activates rules in `.torusguard/rules/active/`, and configures the 5 specialist agents.
- **Triggering:** Invoked conversationally or via slash commands (`/torusguard audit`, `verify`, `harden`, `apply`, `recheck`, `report`).
- **Context Handling:** Reads active workspace AST directly from the IDE's local file system with zero context bloat.

### 2.2. Topology B: CI/CD Pipeline Enforcement
- **Mechanism:** Executed as a standalone step in automated build pipelines.
- **Example GitHub Actions Workflow:**
```yaml
name: TorusGuard Security Gate
on: [push, pull_request]

jobs:
  security-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Run Core Test Harnesses
        run: |
          python harness/runner.py
          python harness/validate_v0_9_2_workflows_and_skills.py
      - name: Export SARIF Security Results
        run: python .torusguard/scripts/sarif_exporter.py --output results.sarif
      - name: Upload SARIF to GitHub Code Scanning
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: results.sarif
          category: torusguard/static
```

### 2.3. Topology C: Air-Gapped / High-Security Environments
- **Zero Egress Guarantee:** TorusGuard contains no telemetry, analytics, or outbound HTTP requests.
- **Offline Operation:** All rules, schemas, and verification logic are bundled locally within the repository.

---

## 3. Resource Requirements & Operational Footprint
- **CPU:** 1 vCPU (scales linearly with multiple cores for large repos).
- **RAM:** $< 250\text{ MB}$ base memory usage.
- **Disk:** $< 15\text{ MB}$ installation footprint + $< 2\text{ MB}$ per audit run folder.
- **OS Compatibility:** Linux (Ubuntu/Debian, Alpine, RHEL), macOS (ARM64, x86_64), Windows (PowerShell/CMD).
