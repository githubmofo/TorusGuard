---
name: torusguard-init
description: Initialize TorusGuard workspace — detect project stack, activate tailored TG-* security rules, and generate SECURITY.md baseline.
version: 0.9.2
workflow: .torusguard/workflows/init.md
tools: Read, Grep, Glob, Write
scripts-binding:
  - .torusguard/scripts/stack_detect.py
---

# TorusGuard Init — Project Stack Discovery & Rule Activation

## Objective
Auto-detect repository technology stack via indicators or `stack_detect.py`, activate framework-tailored `TG-*` security rules into `.torusguard/rules/active/`, and provision `torusguard.json` and `SECURITY.md`.

---

## Pre-Flight Check
1. Verify `.torusguard/` layout (`config/`, `rules/active/`, `runs/`, `scripts/`, `workflows/`, `templates/`, `schemas/`).
2. If missing, unpack via `python skills/torusguard/bootstrap.py --target .`.
3. Check existing `.torusguard/config/torusguard.json` before overwriting.

---

## Execution Steps

1. **Stack Detection:** Run `python .torusguard/scripts/stack_detect.py .` to detect:
   - Python: Django (`manage.py`), FastAPI (`fastapi`), Flask (`flask`), SQLAlchemy.
   - Node: Next.js (`"next"`), Express (`"express"`), React/Vite (`"vite"`).
   - BaaS: Supabase (`@supabase/supabase-js`), Firebase (`firebase-admin`).
2. **Handle CLI Failures:** If `stack_detect.py` crashes or is unable to determine the stack, YOU must manually analyze the directory structure and determine the stack.
3. **Emit Stack Record:** Log detected language, framework, ORM, and client SDKs.
4. **Activate Tailored Rules:** Copy matching `TG-*` rules from `.torusguard/rules/` into `.torusguard/rules/active/`.
5. **Provision Policy:** Create `SECURITY.md` if absent, configuring responsible disclosure contacts.
6. **Write Configuration:** Persist detected stack and active rules count to `.torusguard/config/torusguard.json`.

---

## Safety Constraints
- Never overwrite custom rules in `.torusguard/rules/active/` without prompt.
- Retain existing `SECURITY.md` if already established by repository owners.
- Strictly read-only detection against source files.

---

## Output Format
```markdown
🛡️ [TorusGuard] Workspace Initialized (AI Assisted)
- Primary Stack: <Detected Stack> | Components: <Backend/Frontend/DB>
- Active Rules: <Count> rules enabled in `.torusguard/rules/active/`
- Configuration: `.torusguard/config/torusguard.json` written
Next: Run `/torusguard audit` to execute static security scan.
```
