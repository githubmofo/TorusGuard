# TorusGuard Interactive Security Playground

Welcome to the TorusGuard Playground! This directory contains intentional, isolated, and safe vulnerability fixtures designed to demonstrate the TorusGuard command engine in under 60 seconds without risking production systems.

---

## 🎯 What's Inside

1. **`vulnerable_fastapi/main.py`** (Python / FastAPI)
   - `TG-INPUT-001`: Unescaped raw string formatting in SQL query.
   - `TG-DB-004`: Cross-tenant invoice data exposure (missing tenant filter).
   - `TG-AGENT-001`: System prompt boundary injection vulnerability.

2. **`vulnerable_nextjs/actions.ts`** (TypeScript / Next.js)
   - `TG-CLIENT-001`: Leaked backend service role key in frontend bundle.
   - `TG-AUTH-003`: Unauthenticated Next.js Server Action state mutation.

---

## ⚡ Quickstart Evaluation (Try It in 60s)

### Step 1: Run Static Audit
```bash
python .torusguard/scripts/run_manager.py create playground-audit
# Run AST audit across the playground files
```

### Step 2: Formulate Governed Patch
```bash
# Formulate surgical unified diff conforming to the Ponytail Protocol (<=35 additions, <=25 deletions)
```

### Step 3: Run Content-Aware Diff Guard
```bash
# Verify proposed patch against diff_guard to ensure zero bypasses or token exposures
python .torusguard/scripts/diff_guard.py path/to/patch.diff
```
