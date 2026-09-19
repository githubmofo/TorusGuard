---
description: TorusGuard Autonomous Security Command Engine — run static security audits, authorized runtime web validation, governed remediation, and SARIF exports.
version: 1.3.6
tools: Read, Grep, Glob, Bash, Edit, Write
agent: auditor
---

# /torusguard — Autonomous Application Security Guardrails

$ARGUMENTS

## Objective
Execute TorusGuard security workflows across polyglot codebases (Python, TypeScript, Go, Rust, Java, C#, PHP, and 16+ ecosystems) using either AI chat slash commands or dedicated terminal CLI commands.

## Execution
Parse the requested action from `$ARGUMENTS` (e.g. `audit`, `verify`, `web-validate`, `exploit-check`, `harden`, `apply`, `rollback`, `recheck`, `recipes`, `report`, `status`, `init`):
1. **If action is omitted or 'status':** View `.torusguard/workflows/status.md` and report posture (or run `npx torusguard status`).
2. **If action is specified:** Load the dedicated workflow from `.torusguard/workflows/<action>.md` and matching skill from `skills/torusguard-<action>/SKILL.md` (or run equivalent CLI command: `npx torusguard <action>`).
3. Follow the phase execution steps defined in the workflow.
