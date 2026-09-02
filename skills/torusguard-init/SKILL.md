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
Initialize TorusGuard within the current workspace by inspecting repository files to auto-detect the tech stack, activating framework-tailored `TG-*` security rules, loading reference guides, and provisioning a baseline `SECURITY.md`.

---

## Pre-Flight Check
Before executing initialization:
1. Check if `.torusguard/` directory structure exists.
2. If missing, run `python skills/torusguard/bootstrap.py --target .` to unpack the bundled template payload:
   ```
   .torusguard/
   ├── config/
   ├── agents/
   ├── workflows/
   ├── rules/active/
   ├── scripts/
   ├── templates/
   ├── schemas/
   ├── references/
   └── runs/
   ```
3. If `.torusguard/config/torusguard.json` already exists, read existing configuration and report whether the project was previously initialized.

---

## Execution Steps

### Step 1: Stack Detection
Inspect indicator files or execute `.torusguard/scripts/stack_detect.py` to identify:
- **Python Frameworks**:
  - Django: Presence of `manage.py`, `django.conf.settings`, or `INSTALLED_APPS` in `settings.py`.
  - DRF: `rest_framework` in `requirements.txt` or `from rest_framework import ...`.
  - FastAPI: `FastAPI()` instantiation or `from fastapi import FastAPI, Depends`.
  - Flask: `Flask(__name__)` instantiation or `from flask import Flask`.
  - Data Layer: `declarative_base()` (SQLAlchemy) or `django.db.models.Model` (Django ORM).
- **TypeScript / Node Frameworks**:
  - Next.js: `package.json` with `"next"` dependency or `app/` / `pages/` directory layout.
  - Express: `package.json` with `"express"` or `express()` server instantiation.
  - React/Vite: `"@vitejs/plugin-react"` or `"react"` + `vite.config.ts`.
- **Cloud / BaaS Providers**:
  - Supabase: `@supabase/supabase-js` or `createClient(...)`.
  - Firebase: `firebase-admin` or `initializeApp(...)`.

### Step 2: Emit Detected Stack Block
Produce the standard detection block:
```markdown
## Detected Stack
- Language: <Python | TypeScript | JavaScript>
- Framework: <Django | FastAPI | Flask | Next.js | Express | React>
- Data Layer: <SQLAlchemy | Django ORM | Prisma | Supabase | Firebase | None>
- Dependency Files: <path/to/dependencies>
- Detection Confidence: Confirmed (<file>:<line>)
```

### Step 3: Activate Tailored Rule Families
Link relevant rule summaries from `.torusguard/rules/` into `.torusguard/rules/active/`:
- **Universal Baseline**: `TG-SEC-*` (secrets), `TG-INPUT-*` (validation), `TG-AUTH-*` (auth barriers).
- **Python / Django**: `TG-DB-004` (tenant scoping), `TG-RATE-001` (throttling), `TG-PLATFORM-*`.
- **Python / FastAPI & Flask**: `TG-INPUT-001` (Pydantic boundaries), `TG-INPUT-002` (SQL injection).
- **Next.js / Node**: `TG-CLIENT-*` (client credential leaks), `TG-PLATFORM-001` (CORS).

### Step 4: Bind Framework Reference Guide
Identify and load the corresponding framework security reference from `.torusguard/references/`:
- Django / DRF → `django-security.md`, `drf-security.md`
- FastAPI → `fastapi-security.md`, `sqlalchemy-security.md`
- Flask → `flask-security.md`, `sqlalchemy-security.md`
- Next.js → `nextjs-security.md`
- Express → `express-security.md`
- React / Vite → `react-vite-security.md`
- Supabase / Firebase → `supabase-security.md`, `firebase-security.md`

### Step 5: Provision SECURITY.md
Check if `SECURITY.md` exists in the repository root. If missing, generate one from `.torusguard/templates/SECURITY.template.md`.

### Step 6: Write Configuration
Write `.torusguard/config/torusguard.json` with detected stack, active rules list, and initialization timestamp.

---

## Safety Constraints
- Read-only inspection of source code; never alter application logic during initialization.
- Never overwrite existing customized `torusguard.json` without explicit user confirmation.
- Only activate rules that correspond to frameworks actually present in the codebase.

---

## Output Format
```markdown
🛡️ [TorusGuard] Project Initialized Successfully!
- Detected Stack: <Framework> (<Language>) · <ORM/Data Layer>
- Active Rules: <Count> tailored rules activated in .torusguard/rules/active/
- Security Policy: SECURITY.md verified
- References Loaded: <reference-guide.md>

Next Step: Run `/torusguard audit` to scan your codebase against active security rules.
```
