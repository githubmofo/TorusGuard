---
description: Baseline project discovery, workspace scaffolding, stack detection, and framework-tailored security rule activation.
tools: Read, Grep, Glob, Bash, Write
version: 0.9.2
agent: profiler
lifecycle-phase: Phase 0 (Baseline Setup)
required-skills:
  - torusguard-init
scripts-binding:
  - .torusguard/scripts/stack_detect.py
---

# /torusguard init — Project Baseline & Workspace Initialization

$ARGUMENTS

---

## Objective
Baseline project discovery, workspace scaffolding, stack detection, and security rule activation.

---

## Mandatory Pre-Flight Context Inspection

Inspect workspace state before running initialization:
1. **Config State (`.torusguard/config/torusguard.json`):** Check if workspace is already initialized. If active, prompt before re-writing.
2. **Project Manifests:** Check root for `package.json`, `manage.py`, `requirements.txt`, `pyproject.toml`, `go.mod`, or `Cargo.toml`.
3. **Disclosure Policy (`SECURITY.md`):** Check for existing responsible disclosure policy.
4. **Bootstrapper:** If `.torusguard/` is absent, invoke `python skills/torusguard/bootstrap.py` to unpack offline assets.
5. **Runtime Preconditions:** Ensure Python 3.10+ is available in the current execution shell.

---

## When to Use /torusguard init

| Trigger Scenario | Recommended Command |
| :--- | :--- |
| First-time onboarding in any repository | Run `/torusguard init` |
| Framework upgrade or major dependency changes | Run `/torusguard init` to refresh tailored rules |
| Repository already configured | Run `/torusguard audit` |
| Inspecting existing configuration | Run `/torusguard status` |
| Testing legal boundaries | Run `/torusguard authorize` |

---

## Execution Steps

1. **Scaffold Directory Topology:** Verify `.torusguard/` structure (`config/`, `rules/active/`, `runs/`, `scripts/`, `workflows/`, `templates/`, `schemas/`).
2. **Execute Stack Detection:**
   ```bash
   python .torusguard/scripts/stack_detect.py .
   ```
3. **Activate Tailored Rules:** Symlink or copy matching security rules from `.torusguard/rules/` into `.torusguard/rules/active/`.
4. **Write Configuration (`.torusguard/config/torusguard.json`):**
   Record detected stack, enabled rules count, timestamp, and runtime constraints.
5. **Verify Initialization:** Assert `.torusguard/config/torusguard.json` and `.torusguard/config/scope.json` exist.

---

## Failure Recovery

- **Script Exit 1 (Detection Failed):** Check Python version (`python --version` >= 3.10) and verify read access to root manifests.
- **Permission Error:** Verify write permissions for `.torusguard/config/` and `.torusguard/rules/active/`.
- **Missing Directories:** Re-run directory scaffolding if any subfolder creation fails.
- **Halt Condition:** If root directory is empty, halt and prompt user to open the project root.

---

## Hallucination Guard

- ❌ Never invent framework dependencies not present in `package.json` or `requirements.txt`.
- ❌ Never overwrite an existing `.torusguard/config/scope.json` containing authorized domains.
- ✅ Always execute `.torusguard/scripts/stack_detect.py` to ground detected technologies.

---

## Output Card Format

```markdown
### 🛡️ TorusGuard Workspace Initialization
- **Primary Framework:** [Detected Stack or None]
- **Components:** [Backend / Frontend / Database]
- **Active Rules:** [Count] rules enabled in `.torusguard/rules/active/`
- **Config:** `.torusguard/config/torusguard.json` generated
- **Scope Template:** `.torusguard/config/scope.json` ready
- **Status:** READY — run `/torusguard audit` to scan codebase
```

---

## Next Steps

1. Run `/torusguard authorize` to define allowed target URLs and legal scan boundaries.
2. Run `/torusguard audit` to execute the baseline static security audit.
