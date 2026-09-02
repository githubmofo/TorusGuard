# /torusguard init — Project Baseline & Workspace Initialization

**Command:** `/torusguard init`  
**Primary Agent:** `profiler` (`.torusguard/agents/profiler.md`)  
**Lifecycle Phase:** Phase 0 (Baseline Setup)

---

## Objective
Detect the target project stack, scaffold the `.torusguard/` workspace configuration, activate framework-tailored security rules in `.torusguard/rules/active/`, and verify that `SECURITY.md` is present.

---

## Execution Steps

### Step 1: Pre-Flight Workspace Inspection
1. Check if `.torusguard/config/torusguard.json` already exists.
2. If already initialized, inform the user and ask if they wish to refresh stack detection and rule bindings.

### Step 2: Stack Discovery
1. Inspect project root for framework manifests:
   - Python: `manage.py`, `settings.py` (Django) · `rest_framework` (DRF) · `FastAPI()` (FastAPI) · `Flask(__name__)` (Flask) · `sqlalchemy` (SQLAlchemy).
   - TypeScript/JavaScript: `package.json` with `next` (Next.js) · `express` (Express) · `react` / `vite` (React/Vite).
   - Backend/Cloud: `@supabase/supabase-js` (Supabase) · `firebase-admin` (Firebase).
2. Generate the canonical stack block:
   ```markdown
   ## Detected Stack
   - Language: <detected language>
   - Framework: <detected framework>
   - Data layer: <detected ORM / database layer>
   - Dependency files: <manifest paths>
   - Detection confidence: Confirmed (<evidence file:line>)
   ```

### Step 3: Tailored Rule Activation
1. Based on detected framework, identify relevant rule families from `rules/`:
   - All projects: `TG-SEC-*`, `TG-INPUT-*`, `TG-AUTH-*`.
   - Python/Django: `TG-DB-004`, `TG-RATE-001`, `TG-PLATFORM-*`.
   - Next.js/React: `TG-CLIENT-*`, `TG-PLATFORM-001`, `TG-AUTH-002`.
2. Activate rule definitions or symlinks under `.torusguard/rules/active/`.

### Step 4: Baseline Security Policy Verification
1. Check if `SECURITY.md` exists in the repository root.
2. If missing, generate `SECURITY.md` from `.torusguard/templates/` or repo template.

### Step 5: Write Configuration
1. Update `.torusguard/config/torusguard.json` with detected stack and active rules list.
2. Output initialization summary:
   ```markdown
   🛡️ [TorusGuard] Project initialized successfully!
   - Detected Stack: <Framework> (<Language>)
   - Active Rules: <Count> rules activated in .torusguard/rules/active/
   - Security Policy: SECURITY.md verified
   
   Next Step: Run `/torusguard audit` to execute your first static security scan.
   ```
