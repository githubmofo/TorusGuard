# TorusGuard Roadmap

## Current Version: 2.1.1

### Completed ✅

- [x] Taint Analysis Engine (source-to-sink graph tracking, multi-stage sanitizers)
- [x] Polyglot AST Walker & Tree-Sitter Parsers (Python, TypeScript, JavaScript, Go)
- [x] Cross-File Interprocedural Dataflow Analysis (call graph & import resolution)
- [x] 88 canonical security rules across 22 architectural families (added TG-INPUT-007 and TG-INPUT-008)
- [x] 7-Signal Calibrated Confidence Scoring (evidence-chain calibration)
- [x] Incremental Hash Cache & Multi-Worker Parallel Scanning
- [x] First-Principles Security Suite (Docker/Container, Git History, ReDoS, AI & RAG)
- [x] 22 terminal CLI commands with standardized 75-column formatting
- [x] Master 7-Stage Pipeline command (`torusguard full`)
- [x] 10 native Model Context Protocol (MCP) tools and 2 living resources with stdio stream isolation
- [x] Multi-modal Vision OCR (Tesseract v5.4.0 with 10MB memory safety bounds on PNG, JPG, WebP)
- [x] Unseen Repositories Tri-Mode Validation Suite (100% pass across 6 unseen ecosystems & 18 canonical skills)
- [x] Line-level reflection module with semantic patching (`find_snippet` / `replace_snippet`)
- [x] Streamlined README with dynamic multi-tier architecture & remediation flowchart
- [x] Ponytail Protocol bounds enforcement (≤35 additions, ≤25 deletions)
- [x] Pre-apply snapshot engine with rollback
- [x] Dynamic SARIF v2.1.0 report generation
- [x] Dark-mode HTML posture dashboards
- [x] Cryptographic authorization token generation
- [x] HTTP security probing with audit headers
- [x] Bounded exploit checking with inert payloads
- [x] Evidence verification against `security_report.md`
- [x] Stack detection (Go, Node.js, Python, Rust, Java, etc.)
- [x] Fail-closed cryptography (panic on entropy failure)
- [x] Path traversal defense in snapshot engine
- [x] SSRF blocking (private IP ranges + AWS metadata)
- [x] DoS resilience (10,000-file limit, 5-minute timeout)
- [x] AI agent integration (Antigravity, Cursor, Claude Code, Windsurf)

---

### v2.0.0-beta (Next)

- [ ] Go `go/ast` native parser for Go source files (replacing regex for Go-specific rules)
- [ ] Worker pool concurrency for parallel file scanning
- [ ] SARIF report with precise `physicalLocation` (file, line, column)
- [ ] `torusguard diff` command for pre-commit security gate
- [ ] `torusguard rules list` and `torusguard rules sync` commands
- [ ] JSON-structured CLI output (`--json` flag on all commands)
- [ ] Configuration file (`.torusguard/config.yaml`) for custom rule overrides

### v2.1.0

- [ ] Support for additional languages: Rust, Java, C#, Ruby, PHP
- [ ] Custom rule authoring (user-defined regex patterns)
- [ ] GitHub Actions marketplace action
- [ ] GitLab CI integration template
- [ ] VS Code extension for inline findings
- [ ] Persistent finding database (SQLite) for trend tracking

### v3.0.0 (Long-term)

- [ ] WebAssembly (WASM) build for browser-based scanning
- [ ] Remote rule distribution (pull rules from a registry)
- [ ] Team dashboards with aggregated posture metrics
- [ ] API server mode for CI/CD webhook integration
- [ ] Plugin system for third-party rule packages
