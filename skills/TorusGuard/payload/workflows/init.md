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
Baseline project discovery, workspace scaffolding, stack detection, and framework-tailored security rule activation.

---

## Mandatory Pre-Flight Context Inspection

Before initializing or re-configuring the workspace security environment, you MUST inspect:

1. **Existing Workspace State (`.torusguard/config/torusguard.json`)** → Check if `.torusguard/` is already initialized. If present, prompt the operator before overwriting active configuration.
2. **Project Manifests & Markers** → Inspect project root for `package.json`, `manage.py`, `requirements.txt`, `pyproject.toml`, `go.mod`, or `Cargo.toml`.
3. **Security Policy Anchor (`SECURITY.md`)** → Verify if the repository already defines a responsible disclosure policy.
4. **Offline Template Payload (`skills/torusguard/payload/`)** → If `.torusguard/` is missing in an external project, invoke `python skills/torusguard/bootstrap.py` to unpack all assets locally.

---

## Objective
Baseline project discovery, workspace scaffolding, stack detection, and framework-tailored security rule activation.

---

## When to Use /torusguard init

| Use `/torusguard init` when... | Use something else when... |
| :--- | :--- |
| First time running TorusGuard in a project | Already initialized → `/torusguard audit` |
| Upgraded framework or added new tech stack | Checking current configuration → `/torusguard status` |
| Rebuilding tailored rules after dependency change | Reviewing legal scope permissions → `/torusguard authorize` |
| Resetting `.torusguard/config/torusguard.json` | Running full end-to-end audit → `/torusguard full` |

---

## Objective
Baseline project discovery, workspace scaffolding, stack detection, and framework-tailored security rule activation.

---

## Execution Steps (Fixed Order)

### Phase 1 — Workspace Scaffolding & Bootstrap Verification
1. Verify presence of `.torusguard/` subdirectories (`config/`, `agents/`, `workflows/`, `scripts/`, `templates/`, `schemas/`, `references/`, `rules/active/`, `runs/`).
2. If missing or incomplete, execute the offline bootstrapper:
   ```bash
   python skills/torusguard/bootstrap.py --target .
   ```

### Phase 2 — Automated Stack Discovery
Execute the stack detection engine across repository files:
```bash
python .torusguard/scripts/stack_detect.py . --json
```
Detect languages, web frameworks, ORMs, and cloud SDKs:
- **Python**: Django (`manage.py`, `settings.py`), DRF (`rest_framework`), FastAPI (`FastAPI()`), Flask (`Flask(__name__)`), SQLAlchemy (`declarative_base()`).
- **TypeScript/Node**: Next.js (`next`), Express (`express`), React/Vite (`@vitejs/plugin-react`).
- **Cloud/BaaS**: Supabase (`@supabase/supabase-js`), Firebase (`firebase-admin`).

### Phase 3 — Tailored Rule Family Activation
Activate relevant rule families under `.torusguard/rules/active/`:
- **Universal Baseline**: `TG-SEC-*` (secrets & tokens), `TG-INPUT-*` (input sanitization), `TG-AUTH-*` (session & auth barriers).
- **Stack-Specific Activation**:
  - Django / DRF: `TG-DB-004` (tenant isolation), `TG-RATE-001` (throttling), `TG-PLATFORM-*`.
  - FastAPI / Flask: `TG-INPUT-001` (Pydantic boundary), `TG-INPUT-002` (SQL injection).
  - Next.js / Express: `TG-CLIENT-*` (client credential leak), `TG-PLATFORM-001` (CORS).

### Phase 4 — Security Policy Verification
Check for `SECURITY.md` in repository root. If missing, copy canonical template:
```bash
python -c "import shutil, os; shutil.copyfile('.torusguard/templates/SECURITY.template.md', 'SECURITY.md') if not os.path.exists('SECURITY.md') else None"
```

### Phase 5 — Save State & Manifest Update
Record detected configuration into `.torusguard/config/torusguard.json`.

---

## Objective
Baseline project discovery, workspace scaffolding, stack detection, and framework-tailored security rule activation.

---

## Failure Recovery & Cascade Rules

```
Script exits 0:     Success — continue pipeline
Script exits 1:     Failure — fallback to heuristic file scan (grep manage.py / package.json)
Script not found:   Run bootstrap.py to restore .torusguard/scripts/
Script times out:   Kill after 30s — fallback to generic stack profile
```

**Hard limit: 3 retries.** If stack detection fails after 3 attempts, ask operator for manual framework confirmation.

---

## Objective
Baseline project discovery, workspace scaffolding, stack detection, and framework-tailored security rule activation.

---

## Hallucination Guard

```
❌ Never guess framework versions without reading manifest files
❌ Never overwrite existing customized torusguard.json without prompting
❌ Never create unapproved directories outside .torusguard/ and project root
❌ Never activate rules for frameworks not detected in the workspace
```

---

## Objective
Baseline project discovery, workspace scaffolding, stack detection, and framework-tailored security rule activation.

---

## Output Card Format

```markdown
🛡️ [TorusGuard] Workspace Initialized Successfully
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Language:         [Detected Language, e.g., Python 3.12 / TypeScript 5.4]
Framework:        [Detected Framework, e.g., FastAPI / Django / Next.js]
Data Layer:       [Detected ORM, e.g., SQLAlchemy / Prisma / Django ORM]
Active Rules:     [Count] rules activated in .torusguard/rules/active/
Security Policy:  SECURITY.md verified in repository root
Config Path:      .torusguard/config/torusguard.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Step: Run `/torusguard audit` to perform your first static security scan.
```

---

## Objective
Baseline project discovery, workspace scaffolding, stack detection, and framework-tailored security rule activation.

---

## Next Steps

| Outcome | Next Command |
| :--- | :--- |
| Workspace initialized and rules active | → `/torusguard audit` to scan codebase |
| Project has runtime APIs or web endpoints | → `/torusguard authorize` to set scope |
| Want end-to-end scan + remediation | → `/torusguard full` |
