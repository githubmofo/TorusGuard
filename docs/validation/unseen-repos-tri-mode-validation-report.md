# TorusGuard Multi-Repository, Tri-Mode & Vision OCR Test Report

**Execution Date:** 2026-09-29 19:17:06  
**Version Tested:** `v2.1.1`  
**Total Repositories Tested:** 6 Unseen Framework Ecosystems  
**Total Skills Exercised:** 18/18 Canonical Skills  
**Operational Modes Covered:** Mode A (Terminal CLI), Mode B (AI Chat Slash Commands), Mode C (Native MCP Tools)  
**Multi-Modal Vision Assets:** PNG, JPG, WebP (Tesseract v5.4.0)  
**Total Verification Duration:** 1.65 seconds  
**Sandbox Deletion Status:** Verified Deleted (`True`)  

---

## 1. Executive Summary Table

| Repository Fixture | Tech Stack & Framework | Operational Mode | Skills Exercised | Findings Caught | Status | Duration |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **sveltekit-drizzle-bun** | SvelteKit 2 / Bun / Drizzle | Mode B (AI Slash Commands) | `6 skills` | **3** | ✅ **PASS** | 0.13s |
| **fastapi-asyncpg-rag** | FastAPI / pgvector / Python 3.12 | Mode C (Native MCP JSON-RPC) | `5 skills` | **4** | ✅ **PASS** | 0.14s |
| **cloud-native-devops** | Docker / Compose / Git History | Mode A (Terminal CLI) | `4 skills` | **4** | ✅ **PASS** | 0.17s |
| **multimodal-vision-ocr** | Vision OCR / PNG, JPG, WebP | All 3 Modes (CLI + Slash + MCP) | `1 skills` | **3** | ✅ **PASS** | 0.51s |
| **kotlin-ktor-service** | Kotlin 2.0 / Ktor 3.0 / Netty | Mode A + Mode B | `6 skills` | **2** | ✅ **PASS** | 0.13s |
| **laravel-inertia-vue** | Laravel 11 / Vue 3 / PHP 8.3 | Mode C + Mode A (Full Pipeline) | `4 skills` | **2** | ✅ **PASS** | 0.09s |

---

## 2. Tri-Mode Operational Distribution & Parity

### Mode A: Terminal CLI Binary (`torusguard`)
- **Repositories Exercised:** `cloud-native-devops`, `kotlin-ktor-service`, `laravel-inertia-vue`.
- **Commands Validated:** `container`, `git-mine`, `status`, `audit`, `recipes`, `full`, `authorize`, `web-validate`, `exploit-check`.
- **Parity Assertion:** 75-column standardized box rendering with Unicode width formatting and ANSI color sequences verified across all commands.

### Mode B: AI Chat Slash Commands (`/torusguard`)
- **Repositories Exercised:** `sveltekit-drizzle-bun`, `kotlin-ktor-service`.
- **Slash Workflows Validated:** `/torusguard init`, `/torusguard audit`, `/torusguard harden`, `/torusguard apply`, `/torusguard recheck`, `/torusguard report`.
- **Parity Assertion:** Successfully enforced Ponytail Protocol bounds (≤35 additions, ≤25 deletions), generated pre-apply `.bak` snapshots in `.torusguard/snapshots/`, and confirmed zero-regression differential recheck closure.

### Mode C: Native MCP Tools (Stdio JSON-RPC 2.0 Server)
- **Repositories Exercised:** `fastapi-asyncpg-rag`, `multimodal-vision-ocr`, `laravel-inertia-vue`.
- **MCP Tools Validated:**
  - `torusguard_ai_guard` (Detected vector search missing tenant partition & indirect prompt injection)
  - `torusguard_redos` (Detected exponential backtracking loops)
  - `torusguard_audit` (Full AST + taint audit)
  - `torusguard_verify` (Live disk line fingerprint verification)
  - `torusguard_status` (Diagnostic overview payload)
  - `torusguard_ocr_scan` (Multi-modal image secret scan)
  - `torusguard://security_report` (Living security ledger resource read)
- **Parity Assertion:** 100% compliant with MCP JSON-RPC 2.0 protocol specifications over stdio.

---

## 3. Multi-Modal Vision OCR Verification Results

| Visual Asset | Format | Injected Secret Type | Extracted Content | Mode Tested | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `aws_cloud_architecture.png` | PNG | `AKIAI44QH8DHBEXAMPLE` | `AWS_ACCESS_KEY_ID = AKIAI44QH8DHBEXAMPLE` | Mode A: `torusguard ocr-scan` | ✅ **PASS** |
| `ide_debug_screenshot.jpg` | JPEG | `ghp_0123456789abcdef...` | `GITHUB_TOKEN = ghp_0123456789...` | Mode B: `/torusguard ocr-scan` | ✅ **PASS** |
| `db_topology.webp` | WebP | `postgres://pgadmin:SuperSecret2026@...` | `DATABASE_URL = postgres://...` | Mode C: `torusguard_ocr_scan` | ✅ **PASS** |

---

## 4. 18 Canonical Skills Matrix & Verification Summary

| # | Skill Name | Lifecycle Domain | Test Mode | Observed Result |
| :-: | :--- | :--- | :--- | :--- |
| 1 | `torusguard-init` | Workspace Discovery | Mode A, B | Profiled SvelteKit, Kotlin, Laravel manifests and initialized `.torusguard/`. |
| 2 | `torusguard-status` | Posture Overview | Mode A, C | Displayed formatted diagnostic card with active rules and run count. |
| 3 | `torusguard-audit` | Static & Taint Scan | Mode A, B, C | Traversed polyglot ASTs; identified secret leaks, DB primary key flaws, and taint paths. |
| 4 | `torusguard-ocr-scan` | Visual Secret Scan | Mode A, B, C | Extracted text from PNG, JPG, and WebP images via Tesseract v5.4.0 within 10MB bounds. |
| 5 | `torusguard-verify` | Evidence Audit | Mode C | Verified live code line matches and fingerprint stability. |
| 6 | `torusguard-harden` | Governed Remediation | Mode B | Enforced Ponytail Protocol line limits (≤35 additions, ≤25 deletions). |
| 7 | `torusguard-apply` | Governed Patch Application | Mode B | Captured byte-for-byte `.bak` backup and applied patch with Human Gate (`--yes`). |
| 8 | `torusguard-recheck` | Differential Re-scan | Mode B | Re-scanned modified files; confirmed fix closure and updated `security_report.md`. |
| 9 | `torusguard-recipes` | Persistent Memory | Mode A | Explored and distilled verified Golden Fix recipes in `.torusguard/memory/`. |
| 10 | `torusguard-report` | Executive Outputs | Mode A, B | Exported OASIS SARIF v2.1.0 logs and rendered dark-mode visual HTML dashboards. |
| 11 | `torusguard-authorize` | Legal Boundaries | Mode A | Generated 16-byte cryptographic ownership proof with TTL boundary (fail-closed). |
| 12 | `torusguard-web-validate` | Runtime Probing | Mode A | Conducted HTTP probing with `X-TorusGuard-Audit` headers & SSRF private IP blocking. |
| 13 | `torusguard-exploit-check` | Exploitability Check | Mode A | Sent bounded inert canary tokens to verify backend error handling safely. |
| 14 | `torusguard-container` | Dockerfile Safety | Mode A, C | Audited root user execution (`TG-CONT-001`) and host socket bind mounts (`TG-CONT-002`). |
| 15 | `torusguard-git-mine` | Git History Mining | Mode A, C | Mined historical git commit diffs (`TG-GIT-001`) and `.git/config` remote URLs (`TG-GIT-002`). |
| 16 | `torusguard-redos` | Regex Complexity | Mode C | Detected nested quantifiers `(a+)+` causing $O(2^n)$ exponential backtracking (`TG-REDOS-001`). |
| 17 | `torusguard-ai-guard` | AI & RAG Defense | Mode C | Audited RAG pipelines for unpartitioned vector searches (`TG-RAG-001`) and indirect injection (`TG-RAG-002`). |
| 18 | `torusguard-full` | Master Pipeline | Mode A, B | Coordinated discovery, audit, validation, remediation, and reporting in closed loop. |

---

## 5. Teardown & Sandboxing Certification
- **Sandbox Root:** `C:\Users\Admin\AppData\Local\Temp\tg_unseen_suite_ym9482lf`
- **Post-Run Cleanup:** All 6 synthetic repositories, temporary git histories, Dockerfiles, and image fixtures were completely deleted using `safe_cleanup`.
- **Filesystem Verification:** `os.path.exists(temp_suite_dir) == False`.
