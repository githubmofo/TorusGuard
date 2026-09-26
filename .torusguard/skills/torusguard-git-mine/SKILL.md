---
name: torusguard-git-mine
description: Mines git commit history, commit diffs, and local repository metadata for leaked credentials, private keys, and historical API tokens via CLI, Chat, or MCP.
version: 2.0.0
workflow: .torusguard/workflows/git-mine.md
tools: Read, Grep, Glob, Write, run_command
scripts-binding:
  - internal/scanner/git_mine.go
  - cmd/torusguard/main.go
  - cmd/torusguard/mcp.go
---

# TorusGuard Git History Secret Mining

## Objective
Inspect local `.git` metadata, remote configurations, and commit logs across the repository's commit history to identify leaked API tokens, private keys, database URIs, and credentials that were committed in past revisions or embedded in remote URLs.

---

## Tri-Mode Execution

### Mode A: Automated CLI Execution
Run Git history mining against current repository or specified target workspace:
```bash
# Mine Git commit history and .git/config in current workspace
torusguard git-mine

# Mine specific repository target
torusguard git-mine --target /path/to/repo
```

### Mode B: In-Session AI Chat Slash Command
Run `/torusguard git-mine` in chat.
The agent executes the compiled Go Git mining engine or MCP tool to inspect commit history logs, detect historical secret leaks, and provide provider revocation guidance.

### Mode C: Native MCP Tool Call
MCP-enabled coding agents (Antigravity, Cursor, Windsurf, Claude Code) call:
```json
{
  "tool": "torusguard_git_mine",
  "arguments": {
    "target": "."
  }
}
```

---

## Supported Patterns & Invariants
- **TG-GIT-001 (Historical Secret Commit):** Detects API keys (OpenAI `sk-...`, AWS `AKIA...`, GitHub `ghp_...`), private certificates, or database credentials introduced in prior git commits even if removed from the current working tree.
- **TG-GIT-002 (Plaintext Remote Credentials):** Flags remote URLs in `.git/config` containing basic authentication credentials (`https://user:token@github.com/...`).
- **TG-GIT-003 (Sensitive File History Tracking):** Detects tracked `.env`, `id_rsa`, `.pem`, or `.key` files in git log metadata that bypass `.gitignore`.

---

## 🏛️ OpenCodeReview Hybrid Architecture Integration
- **Deterministic History Inspection:** Analyzes commit logs via local Git commands or fallback file reading with strict 5-second timeouts and bounded commit depths.
- **Token Minimization:** Emits commit SHA, author timestamp, and redacted secret preview rather than dumping full commit logs into LLM context.
- **Revocation-First Governance:** Prioritizes immediate credential revocation at the provider (OpenAI, AWS, GitHub) before history rewrites (`git filter-repo` / BFG).

---

## 🚨 LLM Trap Table

| Pattern | What AI Does Wrong | What Is Actually Correct |
| :--- | :--- | :--- |
| **Working Tree Only Bias** | Only scans files currently on disk, assuming deleted secrets are safely removed. | Always mine Git commit history (`git log -p`) because Git never forgets past commits. |
| **Token in Remote Origin URL** | Recommends `git remote set-url origin https://ghp_xxx@github.com/...` which writes token to disk in plaintext. | Use SSH keys, GitHub CLI (`gh auth login`), or credential helpers (`git credential-manager`). |
| **History Rewriting Over Revocation** | Recommends scrubbing Git history before revoking the leaked secret at the cloud provider. | Always rotate and revoke the credential immediately at the provider first; assume it was scraped. |
| **Single Commit Amends** | Recommends `git commit --amend` when the secret was committed 5 commits ago. | Use `git rebase -i` or `git-filter-repo` for deeper historical scrubbing. |
| **Tracking .env in Git** | Adds `.env` to `.gitignore` without running `git rm --cached .env`, leaving file tracked. | Run `git rm --cached <file>` so Git stops tracking the sensitive file in subsequent commits. |

---

## ✅ Pre-Flight Self-Audit

Before concluding a Git repository security audit, verify:
- [ ] Is `.git` directory present and valid?
- [ ] Were remote URLs in `.git/config` checked for embedded plaintext passwords or tokens?
- [ ] Were the most recent 50 commits audited for added secrets in commit diffs?
- [ ] Did I verify whether `.env` or private keys were ever tracked in git history?
- [ ] Was the user instructed to rotate/revoke leaked keys at the provider immediately?

---

## 🔁 VBC Protocol (Verify → Build → Confirm)

```
VERIFY: Confirm workspace is a valid Git repository with accessible commit history.
BUILD:  Execute torusguard git-mine or torusguard_git_mine to detect historical leaks and credential configs.
CONFIRM: Provide immediate rotation steps, clean .git/config, and scrub historical commits via git-filter-repo.
```
