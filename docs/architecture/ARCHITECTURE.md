# TorusGuard System Architecture

## Table of Contents
1. [System Overview](#1-system-overview)
2. [Design Principles](#2-design-principles)
3. [High-Level Architecture](#3-high-level-architecture)
4. [Module Dependency Map](#4-module-dependency-map)
5. [Command Lifecycle](#5-command-lifecycle)
6. [Technology Stack](#6-technology-stack)
7. [Security Architecture](#7-security-architecture)
8. [Failure Handling & Resilience](#8-failure-handling--resilience)

---

## 1. System Overview

**TorusGuard** is an autonomous security guardrail and remediation engine for AI-built codebases. It operates across three complementary operational modes (**Tri-Mode Parity**):

- **CLI Mode (Mode A):** Deterministic scanning and enforcement running in terminal or CI/CD pipelines via the `torusguard` binary.
- **AI Agent Mode (Mode B):** Chat slash commands (`/torusguard audit`, `/torusguard ocr-scan`, etc.) bridging developer requests to workflow scripts.
- **Native MCP Mode (Mode C):** Standard Model Context Protocol (MCP) JSON-RPC 2.0 stdio server enabling agents (Antigravity, Cursor, Windsurf, Claude Code) to invoke tools natively (`torusguard_audit`, `torusguard_ocr_scan`, `torusguard_harden`) and read live posture resources.

The Go binary handles all deterministic operations (AST scanning, bounds checking, snapshotting, reporting, OCR image analysis), while AI agents handle intelligence-requiring tasks (patch generation, root-cause analysis, remediation formulation).

---

## 2. Design Principles

| Principle | Implementation |
| :--- | :--- |
| **Tri-Mode Parity** | Terminal CLI, Chat Slash Commands, and Native MCP Tools share identical validation rules. |
| **Multi-Modal Vision OCR** | High-accuracy Tesseract OCR scanning for diagrams/mockups with 10MB memory safety bounds. |
| **Single Binary Engine** | Standalone `torusguard.exe` / `torusguard` binary for cross-platform execution. |
| **Fail-Closed** | Crypto failures panic. Scanner aborts on resource exhaustion. |
| **Deterministic** | Same input always produces the exact same scan results. |
| **Ponytail Protocol** | Patches bounded to ≤35 additions, ≤25 deletions per bundle. |
| **Human Gate** | No code is modified without explicit `--yes` confirmation. |
| **Snapshot-First** | Pre-apply `.bak` backups are mandatory before every modification. |

---

## 3. High-Level Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                   cmd/torusguard/main.go & mcp.go                      │
│             (17-command router & JSON-RPC 2.0 MCP Server)              │
└──────────┬───────────┬──────────┬────────────┬───────────┬─────────────┘
           │           │          │            │           │
    ┌──────▼──┐  ┌─────▼────┐ ┌──▼──────┐ ┌───▼──────┐ ┌──▼───────────┐
    │ scanner │  │  apply    │ │validate │ │  report  │ │ mcp server  │
    │         │  │  snapshot │ │authorize│ │  sarif   │ │ stdio RPC   │
    │ AST scan│  │  rollback │ │web-val  │ │  html    │ │ 5 tools     │
    │ ocr.go  │  └─────┬────┘ │exploit  │ └────┬─────┘ │ 2 resources │
    └────┬────┘        │      │verify   │      │       └─────────────┘
         │       ┌─────▼────┐ └────┬────┘ ┌───▼──────┐
    ┌────▼────┐  │  harden  │      │      │  termui  │
    │  rules  │  │ ponytail │      │      │  75-col  │
    │ catalog │  └──────────┘      │      └──────────┘
    └─────────┘                ┌───▼──────┐
                               │workspace │
                               │  init    │
                               │  detect  │
                               └──────────┘
```

---

## 4. Module Dependency Map

| Package | Path | Responsibility | Depends On |
| :--- | :--- | :--- | :--- |
| `main` | `cmd/torusguard/` | CLI entry point, command routing, stdio MCP server (`mcp.go`) | All internal packages |
| `scanner` | `internal/scanner/` | Polyglot AST/heuristic scanner (`scanner.go`) & Vision OCR (`ocr.go`) | `rules` |
| `rules` | `internal/rules/` | Load and manage TG-* rule catalog from `.torusguard/rules/` | — |
| `apply` | `internal/apply/` | Patch application via `git apply`, pre-apply `.bak` snapshots | — |
| `harden` | `internal/harden/` | Ponytail Protocol line-count bounds enforcement (≤35 add, ≤25 del) | — |
| `validate` | `internal/validate/` | Authorization tokens, HTTP probing, SSRF defense, evidence verification | — |
| `report` | `internal/report/` | SARIF v2.1.0 and HTML report generation, `security_report.md` sync | — |
| `recheck` | `internal/recheck/` | Differential re-scan of modified files | — |
| `memory` | `internal/memory/` | Golden Fix recipe persistence and retrieval | — |
| `workspace` | `internal/workspace/` | Workspace initialization and polyglot stack detection | — |
| `termui` | `internal/termui/` | 75-column terminal formatting with Unicode emoji width calculation | — |

---

## 5. Command Lifecycle

```
User Input → main.go Router → Package Handler → Disk I/O → Terminal Output
                                    │
                                    ├── Scanner: Walk files → Regex match → Findings
                                    ├── Apply: Parse patch → Snapshot target → git apply
                                    ├── Harden: Count +/- lines → Assert bounds
                                    ├── Validate: Generate token / HTTP probe / Verify evidence
                                    └── Report: Load findings → Marshal SARIF/HTML → Write file
```

### Audit Command Flow
1. Load rule catalog from `.torusguard/rules/`
2. Walk the target directory (respecting skip patterns: `node_modules`, `.git`, `.torusguard`)
3. For each file: check 5MB size limit → read file → run regex patterns → collect findings
4. Abort if file count exceeds 10,000 or timeout exceeds 5 minutes
5. Sync findings to `security_report.md`

### Apply Command Flow
1. Parse `.patch` file to extract target filename from `--- a/` header
2. Resolve target file path; reject if it escapes workspace boundary
3. Create timestamped `.bak` snapshot of target file in `.torusguard/snapshots/<run_id>/`
4. Execute `git apply` on the patch file
5. Report success or failure

---

## 6. Technology Stack

| Layer | Technology | Rationale |
| :--- | :--- | :--- |
| Language | Go 1.25 | Zero-dependency single binary, cross-platform compilation |
| Scanner | `regexp` + `filepath.Walk` | No CGO required; works on Windows without MinGW/GCC |
| Patch Application | `os/exec` → `git apply` | Leverages Git's robust unified diff parser |
| Token Generation | `crypto/rand` | Cryptographically secure; panics on failure |
| SSRF Defense | `net.LookupIP` + manual range checks | Resolves hostnames before HTTP requests |
| HTTP Probing | `net/http` | Standard library HTTP client with 5-second timeout |
| Reporting | `encoding/json` | Native JSON marshaling for SARIF v2.1.0 |
| Terminal UI | ANSI escape codes | No external TUI library dependency |

---

## 7. Security Architecture

### Self-Protection Measures

TorusGuard enforces the same security standards on itself:

1. **Fail-Closed Entropy**: `generateToken()` panics if `crypto/rand.Read()` fails.
2. **Path Traversal Defense**: `CreateSnapshot()` sanitizes paths with `filepath.Clean()` and rejects `../` escapes.
3. **DoS Resilience**: Scanner limits: 5MB per file, 10,000 files total, 5-minute `context.WithTimeout`.
4. **SSRF Blocking**: `checkSSRF()` resolves hostnames and blocks private IP ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) and AWS metadata (`169.254.169.254`).

### Trust Boundaries

```
┌─────────────────────────────┐
│     AI Agent (Intelligence) │  ← Generates patches, analyzes findings
│     Cursor / Claude / etc.  │
└──────────┬──────────────────┘
           │ Patch file (.patch)
           ▼
┌─────────────────────────────┐
│   TorusGuard CLI (Enforcer) │  ← Validates bounds, snapshots, applies
│   Deterministic Go Binary   │
└──────────┬──────────────────┘
           │ Modified source files
           ▼
┌─────────────────────────────┐
│     Target Codebase         │  ← The project being secured
└─────────────────────────────┘
```

---

## 8. Failure Handling & Resilience

| Failure Mode | Response |
| :--- | :--- |
| `crypto/rand` entropy failure | `panic()` — fail-closed, no fallback |
| File > 5MB | Skip file, continue scan |
| File count > 10,000 | Abort scan with error message |
| Scan exceeds 5 minutes | Abort via `context.WithTimeout` |
| Target file not found for patch | Return error, do not modify any files |
| Path traversal detected in snapshot | Return error, block snapshot creation |
| SSRF to private IP detected | Return error, block HTTP request |
| `git apply` fails | Return error, snapshot remains intact for rollback |
| `security_report.md` missing | Warn user, suggest running `torusguard audit` first |
