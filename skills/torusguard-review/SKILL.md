---
name: torusguard-review
description: Differential PR and Git diff incremental security review — detects newly introduced vulnerabilities between Git branches or commits with net security score deltas.
tools: Read, Grep, Glob, Bash, Edit, Write
version: 2.1.3
last-updated: 2026-10-01
skills:
  - torusguard
  - torusguard-audit
---

# TorusGuard Review — Differential Incremental PR Review

TorusGuard Review performs rapid, surgical security review on Git changes (e.g. against `HEAD~1`, `main`, or PR target branch), analyzing only modified lines to prevent introducing security regressions.

## Invocation

- **Mode A (Terminal CLI):** `torusguard review [--diff <ref>]`
- **Mode B (AI Chat Slash Command):** `/torusguard review` or `/torusguard-review`
- **Mode C (Native MCP Tool):** `torusguard_review(target=".", diff_ref="HEAD~1")`

## Core Capabilities

1. **Sub-300ms Turnaround:** Only parses and checks modified/added lines in Git diffs.
2. **Net Security Score Delta:** Tracks introduced vs. resolved vulnerabilities (`+0 Introduced, -2 Resolved`).
3. **PR Gate Decision:** Blocks CI/CD pipelines if Critical or High severity flaws are introduced.
4. **Alibaba OpenCodeReview Parity:** Outputs ready-to-post pull request inline review comments.
