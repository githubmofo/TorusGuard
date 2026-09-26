---
name: torusguard-init
description: Initialize TorusGuard workspace — detect project stack, activate tailored TG-* security rules, and generate SECURITY.md baseline via CLI or AI Agent.
version: 2.0.0
workflow: .torusguard/workflows/init.md
tools: Read, Grep, Glob, Write, run_command
scripts-binding:
  - internal/scanner/scanner.go
  - .torusguard/scripts/report_sync.py
  - .torusguard/scripts/stack_detect.py
---

# TorusGuard Init — Project Stack Discovery & Rule Activation

## Objective
Auto-detect repository technology stack across 16+ languages and frameworks, provision the `.torusguard/` workspace structure, activate tailored `TG-*` security rules into `.torusguard/rules/active/`, and generate `SECURITY.md` baseline policies.

---

## Tri-Mode Parity

| Mode | Command / Tool | Governed Behavior |
| :--- | :--- | :--- |
| **Mode A: CLI Terminal** | `torusguard init` | Profiles workspace, provisions directories, activates tailored rules. |
| **Mode B: AI Chat Slash** | `/torusguard init` | Inspects workspace dependencies and guides baseline rule activation. |
| **Mode C: Native MCP Tool**| — | Workspace initialization is an administrative setup command. |

---

## Tri-Mode Execution

### Mode A: Automated CLI Execution
Run the workspace initializer from your terminal:
```bash
# Initialize current repository
torusguard init

# Initialize specific directory
torusguard init ./my-app

# Force re-initialization (overwriting existing configuration)
torusguard init --force

# Explicitly specify stack (e.g. react, nextjs, django, fastapi, express, go)
torusguard init --stack express
```

**Under the Hood:**
- Inspects package files (`package.json`, `pyproject.toml`, `requirements.txt`, `go.mod`, `Cargo.toml`, `Gemfile`, `composer.json`, `*.csproj`).
- Detects backend frameworks, frontend libraries, ORMs (Prisma, Mongoose, SQLAlchemy, Django ORM, GORM), and authentication systems.
- Scaffolds `.torusguard/` directory tree: `config/`, `rules/active/`, `runs/`, `scripts/`, `workflows/`, `templates/`, `schemas/`, `memory/`, `snapshots/`.
- Copies tailored rule definitions into `.torusguard/rules/active/`.
- Provisions `SECURITY.md` with standard responsible disclosure contacts.
- Writes `.torusguard/config/torusguard.json`.
- Displays 75-column terminal cards.

### Mode B: In-Session AI Chat Agent Initialization
When initializing a workspace directly in AI chat:
1. **Detect Stack:** Inspect root files (`package.json`, `go.mod`, `requirements.txt`, etc.) to determine languages and frameworks.
2. **Bootstrap Structure:** Ensure `.torusguard/` structure exists.
3. **Activate Rules:** Populate `.torusguard/rules/active/` with applicable rule files from `rules/`.
4. **Provision Policy:** Create `SECURITY.md` if not already present.
5. **Write Configuration:** Persist settings into `.torusguard/config/torusguard.json`.
6. **Prompt Audit:** Advise the user to run `torusguard audit` or `/torusguard audit`.

### Mode C: Native MCP Tool Integration
For autonomous AI coding agents (Antigravity, Cursor, Windsurf, Claude Code):
- **Administrative Provisioning:** Agents prompt or invoke `torusguard init` to scaffold workspace boundaries.
- **Posture Verification:** Once initialized, agents query `torusguard_status` via MCP to inspect active rules and verify initialization state.

---

## Output Card Format
```markdown
### 🛡️ TorusGuard Workspace Initialized Successfully
- **Primary Stack:** Node.js / React / Express
- **Active Rules:** 74 canonical security rules enabled in `.torusguard/rules/active/`
- **Configuration:** Written to `.torusguard/config/torusguard.json`
- **Security Policy:** Baseline `SECURITY.md` generated
- **Next Step:** Run `torusguard audit` or `/torusguard audit` to scan for flaws
```

## Living Report Ground Truth
- Read `security_report.md` in the workspace root before taking any action. Update the relevant finding card after completing remediation.

---

## 🚨 LLM Trap Table

| Pattern | What AI Does Wrong | What Is Actually Correct |
| :--- | :--- | :--- |
| **Destructive Overwrite** | Overwrites user-customized `.torusguard/rules/active/` without checking `--force`. | Preserve existing customized rules unless `--force` is explicitly provided. |
| **Generic Stack Guess** | Guesses Node.js without reading `go.mod`, `pyproject.toml`, or `Cargo.toml` in the repository. | Check actual package manifests to detect real multi-language frameworks. |
| **Root Directory Clutter** | Spills temporary configuration files across root instead of isolating inside `.torusguard/config/`. | Confine all configuration, snapshots, and run artifacts strictly within `.torusguard/`. |
| **Missing SECURITY.md** | Fails to verify whether responsible disclosure policy already exists before creating a new one. | Check for existing `SECURITY.md` at workspace root; avoid clobbering existing policies. |

---

## ✅ Pre-Flight Self-Audit

Before initializing a workspace:
- [ ] Did I inspect root manifests (`go.mod`, `package.json`, etc.) to identify the true technology stack?
- [ ] Did I verify whether `.torusguard/` is already initialized?
- [ ] Did I check if `SECURITY.md` already exists before writing?
- [ ] Are all directories properly scoped to `.torusguard/`?

---

## 🔁 VBC Protocol (Verify → Build → Confirm)

```
VERIFY:  Check workspace root for manifest files and existing .torusguard configuration.
BUILD:   Generate directory tree, configure tailored TG-* rules, and draft SECURITY.md.
CONFIRM: Verify .torusguard/config/torusguard.json is valid JSON and notify user of readiness.
```
