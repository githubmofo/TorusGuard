# TorusGuard — Claude Code Instructions

TorusGuard is an autonomous security engine. When working in a TorusGuard workspace, follow these rules:

## Core Rules

1. **Check `security_report.md` first.** Before writing or modifying code, read the current security posture ledger at the workspace root.
2. **Ponytail Protocol.** All security patches must be surgical diffs: ≤35 line additions, ≤25 line deletions. Never rewrite entire files.
3. **Never introduce security bypasses.** Do not insert `# nosec`, `verify=False`, `InsecureSkipVerify: true`, `csrf().disable()`, or `[AllowAnonymous]`.
4. **Secrets belong in environment variables.** Never hardcode API keys, database credentials, JWT secrets, or service role keys in source code.
5. **Parameterize all SQL.** Never use string interpolation in SQL queries. Use parameterized queries or ORM methods.
6. **Tenant isolation.** Always scope database lookups by tenant or user ownership.

## Available Commands

Run these via the terminal or as slash commands in chat:

```
torusguard init           # Initialize workspace
torusguard audit          # Run security + OCR scan; sync security_report.md
torusguard ocr-scan       # Scan diagram/image assets for leaked credentials
torusguard container      # Audit Dockerfile & Compose for root users & sockets
torusguard git-mine       # Mine git commit history & config for leaked secrets
torusguard redos          # Analyze regex patterns for catastrophic backtracking
torusguard ai-guard       # Scan AI/LLM code for prompt injection & RAG flaws
torusguard verify         # Check evidence sufficiency
torusguard harden         # Validate patch bounds (<=35 add, <=25 del)
torusguard apply --yes    # Apply patch with snapshot
torusguard rollback       # Restore from snapshot
torusguard recheck        # Re-scan modified files
torusguard report --html  # Generate HTML report
torusguard report --sarif # Generate SARIF report
torusguard mcp            # Start Model Context Protocol stdio server
torusguard authorize      # Generate auth token
torusguard web-validate   # Probe running app
torusguard exploit-check  # Send inert test payloads
```

### Native MCP Tools
When Claude Code is connected to TorusGuard via MCP (`mcp_config.json`), invoke native tools directly:
- `torusguard_audit`: Run polyglot AST + Vision OCR scan; writes `security_report.md`
- `torusguard_ocr_scan`: Analyze images/diagrams for leaked API keys and tokens
- `torusguard_container`: Audit container configs for root execution and socket leaks
- `torusguard_git_mine`: Mine git history for historical secrets and token leaks
- `torusguard_redos`: Analyze regexes for catastrophic exponential backtracking
- `torusguard_ai_guard`: Audit LLM prompts, tool registries, and vector queries
- `torusguard_verify`: Asserts evidence sufficiency & line-shift invariant fingerprint matches
- `torusguard_harden`: Validate proposed diff against Ponytail bounds
- `torusguard_recheck`: Differential re-scan confirming zero regressions
- `torusguard_status`: Inspect detected stack and active security rules
- `torusguard://security_report`: Read living security report resource
- `torusguard://rules_catalog`: Explore verified rules catalog & Golden Fix patterns

## Architecture

- **Go CLI binary & MCP Server** at `cmd/torusguard/main.go` and `cmd/torusguard/mcp.go`.
- **Internal packages** at `internal/` — scanner (including `ocr.go`, `container.go`, `git_mine.go`, `redos.go`, `ai_guard.go`), apply, validate, harden, report, rules, workspace, memory, recheck, termui.
- **86 rules across 22 families** — loaded from `.torusguard/rules/`.
- **Snapshot engine** — creates `.bak` files in `.torusguard/snapshots/` before every modification.

## Security Invariants

- The CLI panics on `crypto/rand` failure (fail-closed, no fallback tokens).
- Path traversal is blocked in the snapshot engine via `filepath.Clean()`.
- The scanner enforces a 10,000-file limit and 5-minute timeout.
- The web validator blocks SSRF to private IP ranges and `169.254.169.254`.
