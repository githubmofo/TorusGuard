---
description: TorusGuard Adaptive Security Memory Engine — view memory stats, export/import intelligence, apply TTL decay, and manage false positives.
tools: Read, Grep, Glob, Bash, Write, run_command
version: 2.0.0
agent: reviewer
lifecycle-phase: Intelligence / Memory
required-skills:
  - torusguard
scripts-binding:
  - internal/memory/recipes.go
  - cmd/torusguard/main.go
  - cmd/torusguard/mcp.go
---

# /torusguard memory — Adaptive Security Memory Engine & Intelligence Management

$ARGUMENTS

---

## Objective
Inspect, manage, export, import, or compact persistent local security memory patterns, context window cards, and Golden Fix Recipes.

---

## Tri-Mode Execution

| Mode | Command / Tool | Execution Method |
| :--- | :--- | :--- |
| **Mode A: Terminal CLI** | `torusguard recipes [list \| show \| export]` | Terminal management of Golden Fix Recipes. |
| **Mode B: AI Chat Slash** | `/torusguard recipes` | Interactive exploration of verified remediation patterns. |
| **Mode C: Native MCP Tool** | `torusguard://rules_catalog` | Programmatic access to catalog rules and distilled patterns. |

---

## Subcommands & Usage

| Command | Action | Description |
| :--- | :--- | :--- |
| `torusguard recipes` | List | Display Golden Fix recipes library |
| `torusguard recipes list` | Catalog | Enumerate verified fix patterns |
| `torusguard recipes export` | Export | Export memory bundle for team sharing |

---

## Privacy & Security Invariants
- Memory files remain strictly local under `.torusguard/memory/` and are always gitignored.
- Memory files are never packaged into release tarballs.
- Export operations only occur when explicitly invoked by user command.
