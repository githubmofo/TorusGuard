---
name: torusguard-init
description: Initialize TorusGuard workspace — detect project stack, activate tailored TG-* security rules, and generate SECURITY.md baseline via CLI or AI Agent.
version: 1.3.4
workflow: .torusguard/workflows/init.md
tools: Read, Grep, Glob, Write, run_command
scripts-binding:
  - .torusguard/scripts/stack_detect.py
  - .torusguard/scripts/term_ui.py
---

# TorusGuard Init — Project Stack Discovery & Rule Activation

## Objective
Auto-detect repository technology stack across 16+ languages and frameworks, provision the `.torusguard/` workspace structure, activate tailored `TG-*` security rules into `.torusguard/rules/active/`, and generate `SECURITY.md` baseline policies.

---

## Two Execution Modes

### Mode A: Automated CLI Execution
Run the workspace initializer from your terminal:
```bash
# Initialize current repository
npx torusguard init

# Initialize specific directory
npx torusguard init ./my-app

# Force re-initialization (overwriting existing configuration)
npx torusguard init --force

# Explicitly specify stack (e.g. react, nextjs, django, fastapi, express)
npx torusguard init --stack express
```
**Under the Hood:**
- Runs `stack_detect.py` to inspect package files (`package.json`, `pyproject.toml`, `requirements.txt`, `go.mod`, `Cargo.toml`, `Gemfile`, `composer.json`, `*.csproj`).
- Detects backend frameworks, frontend libraries, ORMs (Prisma, Mongoose, SQLAlchemy, Django ORM), and authentication systems.
- Scaffolds `.torusguard/` directory tree: `config/`, `rules/active/`, `runs/`, `scripts/`, `workflows/`, `templates/`, `schemas/`, `memory/`, `snapshots/`.
- Copies tailored rule definitions into `.torusguard/rules/active/`.
- Provisions `SECURITY.md` with standard responsible disclosure contacts.
- Writes `.torusguard/config/torusguard.json`.
- Displays 75-column terminal cards.

### Mode B: In-Session AI Chat Agent Initialization
When initializing a workspace directly in AI chat:
1. **Detect Stack:** Inspect root files (`package.json`, `requirements.txt`, etc.) to determine languages and frameworks.
2. **Bootstrap Structure:** Ensure `.torusguard/` structure exists. If missing, run `python skills/torusguard/bootstrap.py --target .`.
3. **Activate Rules:** Populate `.torusguard/rules/active/` with applicable rule files from `rules/`.
4. **Provision Policy:** Create `SECURITY.md` if not already present.
5. **Write Configuration:** Persist settings into `.torusguard/config/torusguard.json`.
6. **Prompt Audit:** Advise the user to run `npx torusguard audit` or `/torusguard audit`.

---

## Output Card Format
```markdown
### 🛡️ TorusGuard Workspace Initialized Successfully
- **Primary Stack:** Node.js / React / Express
- **Active Rules:** 71 canonical security rules enabled in `.torusguard/rules/active/`
- **Configuration:** Written to `.torusguard/config/torusguard.json`
- **Security Policy:** Baseline `SECURITY.md` generated
- **Next Step:** Run `npx torusguard audit` or `/torusguard audit` to scan for flaws
```
