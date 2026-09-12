# TorusGuard API & Skill Interface Specification

## 1. Overview
This document specifies the formal application programming interfaces, CLI command dispatchers, skill contracts, and schema payloads utilized by TorusGuard as of **v1.3.5**.

---

## 2. Command & Dispatch Interface (14 Operations)

TorusGuard enforces 100% functional parity between **Mode A (Terminal CLI: `npx torusguard <cmd>`)** and **Mode B (AI Chat: `/torusguard <cmd>`)**:

| Operation | Mode A (CLI) | Mode B (Chat) | Bound Implementation | Artifacts Generated |
| :--- | :--- | :--- | :--- | :--- |
| **1. Init** | `npx torusguard init` | `/torusguard init` | `stack_detect.py`, `bootstrap.py` | `.torusguard/config/torusguard.json`, `SECURITY.md` |
| **2. Status** | `npx torusguard status` | `/torusguard status` | `bin/torusguard.js status` | 75-column diagnostic posture card |
| **3. Audit** | `npx torusguard audit` | `/torusguard audit` | `audit_runner.py`, `report_sync.py` | `security_report.md`, `findings.json` |
| **4. Verify** | `npx torusguard verify` | `/torusguard verify` | `finding_scorer.py --verify` | Evidence verification & calibrated scores |
| **5. Harden** | `npx torusguard harden` | `/torusguard harden` | `harden_runner.py` | `.torusguard/runs/<run_id>/bundles/` |
| **6. Apply** | `npx torusguard apply [--yes]` | `/torusguard apply` | `apply_runner.py` | Pre-apply snapshots in `.torusguard/snapshots/` |
| **7. Rollback** | `npx torusguard rollback` | `/torusguard rollback`| `apply_runner.py --rollback` | Source restoration from `.torusguard/snapshots/` |
| **8. Recheck** | `npx torusguard recheck` | `/torusguard recheck` | `recheck_runner.py`, `report_sync.py`| Closed findings, updated `security_report.md` |
| **9. Recipes** | `npx torusguard recipes` | `/torusguard recipes` | `recipes_runner.py` | Distilled patterns in `memory/patterns.json` |
| **10. Report** | `npx torusguard report --html`| `/torusguard report` | `html_reporter.py`, `sarif_exporter.py`| `report-latest.html`, `results.sarif` |
| **11. Authorize**| `npx torusguard authorize` | `/torusguard authorize` | `safety_gate.py --authorize` | `.torusguard/config/scope.json` |
| **12. Validate** | `npx torusguard web-validate` | `/torusguard web-validate`| `safety_gate.py --validate` | Bounded HTTP trace logs with scrubbed secrets |
| **13. Exploit** | `npx torusguard exploit-check`| `/torusguard exploit-check`| `safety_gate.py --exploit` | Exploitability confirmation matrix |
| **14. Rules Sync**| `npx torusguard rules sync` | `/torusguard rules sync` | `rules_sync.py` | `.cursorrules`, `CLAUDE.md`, `.windsurfrules` |

---

## 3. Schema Contracts & Data Models

TorusGuard enforces JSON Schema Draft-07 contracts for all structured interchange payloads:

### 3.1. Finding Contract (`schemas/finding.schema.json`)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["finding_id", "rule_id", "file_path", "line_number", "severity", "confidence_score", "status"],
  "properties": {
    "finding_id": { "type": "string" },
    "rule_id": { "type": "string", "pattern": "^TG-[A-Z]+-[0-9]{3}$" },
    "file_path": { "type": "string" },
    "line_number": { "type": "integer", "minimum": 1 },
    "fingerprint": { "type": "string" },
    "severity": { "enum": ["Critical", "High", "Medium", "Low", "Informational"] },
    "confidence_score": { "type": "integer", "minimum": 0, "maximum": 100 },
    "status": { "enum": ["OPEN", "VERIFIED", "CANDIDATE", "APPLIED", "RESOLVED", "REGRESSED", "FALSE POSITIVE"] }
  }
}
```

### 3.2. Golden Recipe Contract (`schemas/golden-recipe.schema.json`)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["recipe_id", "rule_id", "framework", "patch_diff", "additions", "deletions", "verified_at"],
  "properties": {
    "recipe_id": { "type": "string" },
    "rule_id": { "type": "string" },
    "framework": { "type": "string" },
    "patch_diff": { "type": "string" },
    "additions": { "type": "integer", "maximum": 35 },
    "deletions": { "type": "integer", "maximum": 25 },
    "verified_at": { "type": "string" }
  }
}
```

---

## 4. Exit Codes & Programmatic Invariants
- `0`: Success (audit completed, patches applied, or recheck clean).
- `1`: Security regression detected, diff guard blocked commit, or out-of-scope authorization violation.
- `2`: Syntax or schema validation failure.
