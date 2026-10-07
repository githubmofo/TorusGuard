# TorusGuard API & Skill Interface Specification

## 1. Overview
This document specifies the formal application programming interfaces, CLI command dispatchers, skill contracts, and schema payloads utilized by TorusGuard as of **v2.2.0**.

---

## 2. Command & Dispatch Interface (Tri-Mode Parity)

TorusGuard enforces 100% functional parity between **Mode A (Terminal CLI)**, **Mode B (AI Chat Slash Command)**, and **Mode C (Native MCP Protocol)** across all 25 lifecycle operations:

| Operation | Mode A: Terminal CLI | Mode B: AI Chat Slash Command | Mode C: Native MCP Tool | Bound Implementation | Artifacts Generated |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **0. Interactive Menu** | `torusguard` / `npx torusguard` | `/torusguard` | — | `cmd/torusguard/main.go` | Interactive 75-col ANSI TTY Menu |
| **1. Init** | `torusguard init` | `/torusguard init` | — | `internal/workspace/` | `.torusguard/`, `security_report.md` |
| **2. Status** | `torusguard status` | `/torusguard status` | `torusguard_status` | `internal/workspace/` | 75-column diagnostic posture card |
| **3. Audit** | `torusguard audit` | `/torusguard audit` | `torusguard_audit` | `internal/scanner/` | `security_report.md`, findings ledger |
| **4. OCR Vision** | `torusguard ocr-scan [target]` | `/torusguard ocr-scan` | `torusguard_ocr_scan` | `internal/scanner/ocr.go` | Optical finding list with redacted secrets |
| **5. Verify** | `torusguard verify` | `/torusguard verify` | `torusguard_verify` | `internal/validate/` | Evidence verification & calibrated scores |
| **6. Harden** | `torusguard harden [patch]` | `/torusguard harden` | `torusguard_harden` | `internal/harden/` | Ponytail-validated patch candidate |
| **7. Apply** | `torusguard apply [--yes]` | `/torusguard apply` | — | `internal/apply/` | Pre-apply snapshots in `.torusguard/snapshots/` |
| **8. Rollback** | `torusguard rollback` | `/torusguard rollback` | — | `internal/apply/` | Source restoration from `.torusguard/snapshots/` |
| **9. Recheck** | `torusguard recheck` | `/torusguard recheck` | `torusguard_recheck` | `internal/recheck/` | Closed findings, updated `security_report.md` |
| **10. Recipes** | `torusguard recipes` | `/torusguard recipes` | `torusguard://rules_catalog` | `internal/memory/` | Golden Fix library inspection |
| **11. Report** | `torusguard report [--html/--sarif]` | `/torusguard report` | `torusguard://security_report` | `internal/report/` | Single-file visual HTML & SARIF v2.1.0 |
| **12. MCP Server** | `torusguard mcp` | — | Stdio JSON-RPC 2.0 | `cmd/torusguard/mcp.go` | Standard MCP session over stdin/stdout |
| **13. Authorize** | `torusguard authorize` | `/torusguard authorize` | — | `internal/validate/` | Cryptographic ownership authorization tokens |
| **14. Validate** | `torusguard web-validate` | `/torusguard web-validate` | — | `internal/validate/` | Bounded HTTP trace logs with scrubbed secrets |
| **15. Exploit** | `torusguard exploit-check` | `/torusguard exploit-check` | — | `internal/validate/` | Exploitability confirmation matrix |
| **16. Container** | `torusguard container` | `/torusguard container` | `torusguard_container` | `internal/scanner/container.go` | Non-root and socket mount finding cards |
| **17. Git Mine** | `torusguard git-mine` | `/torusguard git-mine` | `torusguard_git_mine` | `internal/scanner/git_mine.go` | Historical commit secret finding cards |
| **18. ReDoS** | `torusguard redos` | `/torusguard redos` | `torusguard_redos` | `internal/scanner/redos.go` | Catastrophic backtracking regex finding cards |
| **19. AI Guard** | `torusguard ai-guard` | `/torusguard ai-guard` | `torusguard_ai_guard` | `internal/scanner/ai_guard.go` | Prompt injection and tenant finding cards |
| **20. Review** | `torusguard review` | `/torusguard review` | `torusguard_review` | `internal/scanner/` | Incremental Git diff and PR gate review |
| **21. Threat Model** | `torusguard threatmodel` | `/torusguard threatmodel` | `torusguard_threatmodel` | `internal/scanner/` | STRIDE threat model & Mermaid DFDs |
| **22. Benchmark** | `torusguard benchmark` | `/torusguard benchmark` | `torusguard_benchmark` | `internal/scanner/` | SecurityReviewBench precision & recall suite |
| **23. Full** | `torusguard full` | `/torusguard full` | — | `skills/torusguard-full` | Master 7-stage closed-loop security governance pipeline |
| **24. Update** | `torusguard update` | `/torusguard update` | — | `bin/torusguard.js` / CLI | Engine self-update inspection |
| **25. Help** | `torusguard help` | `/torusguard help` | — | `cmd/torusguard/` | Interactive command guide |

---

## 2.1. Model Context Protocol (MCP) Tool Contracts

AI coding agents discover and execute TorusGuard tools natively via stdio JSON-RPC 2.0:

### `torusguard_audit`
- **Description:** Runs polyglot static AST scan & multi-modal Vision OCR on target directory, writing results to `security_report.md`.
- **Parameters:** `target` (string, default: `"."`), `include_ocr` (boolean, default: `true`), `max_image_mb` (integer, default: `10`).

### `torusguard_ocr_scan`
- **Description:** Scans an image file or directory of diagrams for leaked secrets using Hybrid First-Principles extraction and optional Tesseract OCR.
- **Parameters:** `target` (string, default: `"."`), `max_image_mb` (integer, default: `10`).

### `torusguard_verify`
- **Description:** Verifies finding evidence sufficiency and audits line-shift invariant fingerprint matches against disk.
- **Parameters:** `target` (string, default: `"."`).

### `torusguard_harden`
- **Description:** Asserts candidate patch conformity to Ponytail bounds (≤35 additions, ≤25 deletions) and blocks security bypasses.
- **Parameters:** `patch_file` (string, default: `"candidate.patch"`).

### `torusguard_recheck`
- **Description:** Differential re-scan verifying that previously flagged findings are Confirmed Fixed with zero regressions.
- **Parameters:** `target` (string, default: `"."`).

### `torusguard_status`
- **Description:** Read-only posture diagnostics and detected framework stack.
- **Parameters:** `target` (string, default: `"."`).

### `torusguard_container`
- **Description:** Audits Dockerfiles, Containerfiles, and Docker Compose configurations for root execution, docker socket exposure, privileged mode, and build-arg secrets.
- **Parameters:** `target` (string, default: `"."`).

### `torusguard_git_mine`
- **Description:** Mines Git commit history, commit diffs, and local repository metadata for leaked credentials, private keys, and historical API tokens.
- **Parameters:** `target` (string, default: `"."`).

### `torusguard_redos`
- **Description:** Analyzes regular expressions across JavaScript, TypeScript, Python, and Go for catastrophic exponential backtracking and ReDoS vulnerabilities.
- **Parameters:** `target` (string, default: `"."`).

### `torusguard_ai_guard`
- **Description:** Audits AI agents, LLM integrations, and RAG pipelines for prompt injection, unsandboxed tool executions, and cross-tenant vector contamination.
- **Parameters:** `target` (string, default: `"."`).

### `torusguard_review`
- **Description:** Analyzes incremental git diffs and pull requests against TorusGuard security invariants and outputs gate decisions.
- **Parameters:** `target` (string, default: `"."`).

### `torusguard_threatmodel`
- **Description:** Synthesizes STRIDE threat model analysis and Mermaid DFD architecture diagrams into `SECURITY_THREAT_MODEL.md`.
- **Parameters:** `target` (string, default: `"."`).

### `torusguard_benchmark`
- **Description:** Executes SecurityReviewBench automated precision and recall test suite.
- **Parameters:** `target` (string, default: `"."`).

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
