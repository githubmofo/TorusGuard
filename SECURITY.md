# Security Policy

## Supported Versions

| Version       | Supported          |
| :------------ | :----------------- |
| 2.0.0-alpha   | ✅ Active development |
| 1.4.x         | ✅ Security patches |
| < 1.4.0       | ❌ End of life      |

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

If you discover a security vulnerability in TorusGuard, please report it responsibly:

1. **Email:** Send a detailed report to the maintainer via GitHub private vulnerability reporting at [github.com/githubmofo/TorusGuard/security/advisories](https://github.com/githubmofo/TorusGuard/security/advisories)
2. **Include:**
   - Description of the vulnerability
   - Steps to reproduce
   - Affected versions
   - Potential impact assessment
   - Suggested fix (if available)

## Response Timeline

| Stage                  | Target     |
| :--------------------- | :--------- |
| Acknowledgment         | 48 hours   |
| Initial assessment     | 5 days     |
| Patch development      | 14 days    |
| Public disclosure       | 30 days after patch |

## Security Design Principles

TorusGuard itself is built following the security principles it enforces:

### Tri-Mode Governance Model
- TorusGuard operates as a strictly enforced **Tri-Track Security Engine**:
  - **Mode A (Terminal CLI):** Deterministic enforcement via the standalone Go binary.
  - **Mode B (AI Chat Slash Commands):** Prompt-guided workflow bridge.
  - **Mode C (Native MCP Protocol):** Standardized JSON-RPC 2.0 stdio tools and resources for direct agent invocation.
- The AI Agent acts purely as an intelligence layer (formulating fixes) and is restricted from bypassing the Go enforcement binary.
- All three modes converge directly into `security_report.md` as the living ground truth to eliminate finding drift or hallucination.

### Multi-Modal Vision OCR Security Controls
- **Resource Exhaustion Bounds:** Image scanning is strictly bounded to a 10MB memory safety envelope (configurable 5MB–10MB) to mitigate decompression bombs and image-based Denial of Service (DoS) attacks.
- **Directory Traversal Defense:** Image file discovery is constrained within the target repository and skips `.git/`, `node_modules/`, and internal system folders.
- **Automated Evidence Redaction:** Extracted secret payloads in OCR evidence strings are automatically truncated and masked prior to logging or streaming over MCP.

### Model Context Protocol (MCP) Boundary Defense
- **Stdio Isolation:** The MCP server communicates strictly over standard input/output using JSON-RPC 2.0; no raw network listeners or unsandboxed RPC ports are opened.
- **Strict Schema Parameter Validation:** Every exposed tool (`torusguard_audit`, `torusguard_ocr_scan`, `torusguard_harden`, `torusguard_recheck`, `torusguard_status`) enforces typed JSON Schema input contracts.
- **Output Truncation Safeguard:** Tool responses are capped at a 32,000-character ceiling (`maxOutputChars = 32000`) to strictly prevent LLM context window saturation attacks.

### Fail-Closed Architecture
- Cryptographic token generation panics on entropy failure rather than falling back to a predictable value.
- The scanner aborts on resource exhaustion (10,000-file limit, 5-minute timeout) rather than producing incomplete results.

### Path Traversal Prevention
- All file paths in the snapshot engine are sanitized with `filepath.Clean()` and validated to prevent directory escape.
- Patch files are parsed to extract target filenames, and the resolved path must stay within the workspace boundary.

### SSRF Defense
- The `web-validate` command resolves target hostnames and blocks requests to private IP ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) and cloud metadata endpoints (`169.254.169.254`).

### Ponytail Protocol (Churn Bounds)
- No patch bundle may exceed 35 line additions or 25 line deletions.
- This prevents full-file rewrites that could introduce unreviewed vulnerabilities.

### Human Gate
- The `apply` command requires explicit `--yes` confirmation before modifying any source file.
- Pre-apply `.bak` snapshots are always captured before modifications.

## Scope

This security policy covers:
- The TorusGuard Go CLI binary (`cmd/torusguard/`) including the MCP server (`cmd/torusguard/mcp.go`)
- The `internal/` packages (scanner, ocr, apply, validate, harden, report, memory, rules, termui, workspace)
- The `.torusguard/` workspace configuration schemas and persistent memory
- The AI agent integration files (`AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `.cursorrules`, `.windsurfrules`, `.agents/mcp_config.json`, `mcp_config.json`)

This security policy does **not** cover:
- Third-party AI agents that consume TorusGuard rules (Cursor, Claude Code, etc.)
- User-authored security rules or custom scanners
- The npm wrapper (`bin/torusguard.js`) which delegates to the Go binary

## Known Security Boundaries

1. **Heuristic Scanner Limitations:** The scanner uses regex-based heuristic analysis rather than full AST parsing. It may produce false negatives on obfuscated or dynamically generated code patterns.
2. **Local-Only Probing:** The `web-validate` and `exploit-check` commands are designed exclusively for `localhost` testing. Pointing them at production systems is outside the intended security boundary.
3. **Agent Trust Model:** When running in AI Agent Mode, TorusGuard relies on the host agent's isolation model. It does not independently sandbox agent-generated code.
