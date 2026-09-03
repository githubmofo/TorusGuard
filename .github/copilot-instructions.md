

# TorusGuard Security Instructions
---
description: TorusGuard Autonomous Security Command Engine — run static security audits, authorized runtime web validation, governed remediation, and SARIF exports.
version: 0.9.2
tools: Read, Grep, Glob, Bash, Edit, Write
agent: auditor
---

# /torusguard — Autonomous Application Security Guardrails

$ARGUMENTS

## Objective
Execute TorusGuard security workflows across Python and TypeScript codebases.

## Execution
Parse the requested action from `$ARGUMENTS` (e.g. `audit`, `verify`, `web-validate`, `exploit-check`, `harden`, `apply`, `recheck`, `report`, `status`, `init`):
1. **If action is omitted or 'status':** View `.torusguard/workflows/status.md` and report posture.
2. **If action is specified:** Load the dedicated workflow from `.torusguard/workflows/<action>.md` and matching skill from `.torusguard/skills/torusguard-<action>/SKILL.md`.
3. Follow the phase execution steps defined in the workflow.
