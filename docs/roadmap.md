# TorusGuard Roadmap

## Current Version: 2.1.0

### Completed ✅

- [x] First-Principles Security Suite (Docker/Container, Git History, ReDoS, AI & RAG)
- [x] 86 rules across 22 architectural families
- [x] 21 terminal CLI commands with 75-column formatting
- [x] 10 native Model Context Protocol (MCP) tools and 2 living resources
- [x] Multi-modal Vision OCR (Tesseract v5.4.0 with 10MB memory safety bounds)
- [x] Line-level reflection module with semantic patching (`find_snippet` / `replace_snippet`)
- [x] Streamlined README with dynamic multi-tier architecture & remediation flowchart
- [x] Heuristic regex-based polyglot scanner (Go, JS, TS, Python)
- [x] Ponytail Protocol bounds enforcement (≤35 additions, ≤25 deletions)
- [x] Pre-apply snapshot engine with rollback
- [x] Dynamic SARIF v2.1.0 report generation
- [x] Dark-mode HTML posture dashboards
- [x] Cryptographic authorization token generation
- [x] HTTP security probing with audit headers
- [x] Bounded exploit checking with inert payloads
- [x] Evidence verification against `security_report.md`
- [x] Stack detection (Go, Node.js, Python, etc.)
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
