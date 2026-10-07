# TorusGuard Roadmap

## Current Version: 2.2.0

### Completed in v2.2.0 & Prior Milestones ✅

- [x] **Hybrid First-Principles Vision OCR:** Built-in zero-dependency stream and metadata extractor (PNG chunks, SVG text, EXIF, printable byte streams) with optional deep optical scanning via Tesseract v5.4.0.
- [x] **Zero-Crash OCR Fallback:** Graceful fallback when Tesseract is missing—never aborts or crashes; auto-discovers all project images.
- [x] **Interactive Terminal Command Center:** Launching `torusguard` or `npx torusguard` with zero arguments renders a menu-driven TTY dashboard.
- [x] **Universal CLI Parity across NPM & Go:** All 25 commands (`ocr-scan`, `container`, `git-mine`, `redos`, `ai-guard`, etc.) wired directly into `bin/torusguard.js` and `cmd/torusguard/main.go`.
- [x] **Curated Awesome Rules Catalog:** Standardized taxonomy of all 88 security invariants across 22 architectural families (`docs/awesome-rules.md`).
- [x] **Taint Analysis Engine:** Source-to-sink graph tracking, cross-file interprocedural dataflow, multi-stage sanitizers.
- [x] **Polyglot AST Walker:** Tree-sitter powered syntax trees across Go, TypeScript, JavaScript, Python.
- [x] **88 Canonical Security Rules:** Covering Secrets, Auth, Tenant DB Isolation, SSRF, Webhooks, CSRF, Supply Chain, Containers, Git History, ReDoS, AI & RAG.
- [x] **7-Signal Calibrated Confidence Scorer:** Evidence-chain calibration combining severity, taint depth, sanitizer checks, and memory.
- [x] **First-Principles Security Suite:** Dockerfile/Compose privileges, Git commit log mining, Thompson NFA ReDoS, RAG vector isolation.
- [x] **Model Context Protocol (MCP) Server:** 13 native JSON-RPC 2.0 tools and 2 living resources with stdio stream isolation.
- [x] **Line-Level Reflection Module:** Semantic patch synthesis (`find_snippet` / `replace_snippet`) preventing line-shift errors.
- [x] **Ponytail Protocol Enforcement:** Strict churn bounds ($\le 35$ additions, $\le 25$ deletions) preventing full-file rewrites.
- [x] **Pre-Apply Snapshot Engine:** Automatic `.bak` backups before modifying files on disk with instant rollback.
- [x] **Standards Compliant Reporting:** OASIS SARIF v2.1.0 exports and single-file dark-mode HTML dashboards.
- [x] **Living Security Report Ground Truth:** Real-time synchronization with `security_report.md` eliminating hallucination.
- [x] **Fail-Closed Cryptography:** Panic on entropy failure; zero hardcoded fallback tokens.
- [x] **SSRF Defense:** Resolves hostnames and blocks private IP ranges (`10.0.0.0/8`) and AWS metadata (`169.254.169.254`).
- [x] **DoS Resilience:** 10,000-file maximum traversal limit and 5-minute scan timeout.

---

### v2.3.0 (Planned)

- [ ] **Native WASM OCR Preprocessor:** In-memory WebAssembly image binarization for enhanced low-contrast text extraction.
- [ ] **Custom Rule Engine:** TG-QL user-defined YAML rule patterns in `.torusguard/rules/custom/`.
- [ ] **Git Pre-Commit Hook Integration:** Zero-latency incremental diff gating via `torusguard review --pre-commit`.
- [ ] **Interactive Remediation TUI:** Terminal cursor-driven patch preview and approval interface.

---

### v3.0.0 (Long-Term Horizon)

- [ ] **WebAssembly (WASM) Engine Build:** Browser-native and edge execution with zero binary installation.
- [ ] **Distributed Rule Registry:** Enterprise private catalog synchronization and team rule distribution.
- [ ] **Centralized Posture Telemetry:** Multi-repository aggregated posture heatmaps and team dashboards.
