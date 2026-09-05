---
description: TorusGuard Adaptive Security Memory Engine — view memory stats, export/import intelligence, apply TTL decay, and manage false positives.
tools: Read, Grep, Glob, Bash
version: 1.0.0
agent: reviewer
lifecycle-phase: Intelligence / Memory
required-skills:
  - torusguard
scripts-binding:
  - .torusguard/scripts/memory_engine.py
---

# /torusguard memory — Adaptive Security Memory Engine & Intelligence Management

$ARGUMENTS

---

## Objective
Inspect, manage, export, import, or compact persistent local security memory patterns, context window cards, and false positive suppressions.

---

## Subcommands & Usage

| Command | Action | Description |
| :--- | :--- | :--- |
| `npx torusguard memory` | Status | Display memory stats, pattern count, and context token estimate |
| `npx torusguard memory context` | Context Dump | Output the active pre-computed context window cards |
| `npx torusguard memory fp --rule <RULE_ID>` | False Positive | Suppress rule as false positive across future scans |
| `npx torusguard memory decay [--ttl 90]` | TTL Decay | Apply confidence decay to stale, unconfirmed patterns |
| `npx torusguard memory export --path <FILE>` | Export | Export memory bundle for team sharing |
| `npx torusguard memory import --path <FILE>` | Import | Merge external memory bundle into local project intelligence |
| `npx torusguard memory compact` | Compaction | Archive raw events older than 30 days into single archive |

---

## Execution Steps

1. **Verify Memory Subsystem:** Confirm `.torusguard/memory/` exists and is shielded by `.gitignore`.
2. **Execute Requested Action:** Invoke `.torusguard/scripts/memory_engine.py` with appropriate action flag:
   ```bash
   python .torusguard/scripts/memory_engine.py --action status
   ```
3. **Verify Context Token Budget:** Confirm `context.json` remains within token budget ($\le 2,000$ tokens).
4. **Display Intelligence Card:** Render summary card to user.

---

## Privacy & Security Invariants
- Memory files remain strictly local under `.torusguard/memory/` and are always gitignored.
- Memory files are never packaged into npm release tarballs.
- Export operations only occur when explicitly invoked by user command.
