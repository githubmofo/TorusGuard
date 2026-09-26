# /torusguard-git-mine — Git Repository & History Secret Mining

$ARGUMENTS

---

## Objective
Inspect local Git metadata, `.git/config` remotes, and historical commit logs to uncover leaked API tokens, private certificates, and sensitive credentials committed in previous revisions.

---

## Tri-Mode Parity
- **Mode A (Terminal CLI):** `torusguard git-mine [target]`
- **Mode B (AI Chat Slash Command):** `/torusguard git-mine [target]`
- **Mode C (Native MCP Tool):** `torusguard_git_mine`

---

## Execution Steps

1. **Verify Git Environment:** Verify target directory is a valid Git repository containing `.git/`.
2. **Audit Remote Configurations:** Check `.git/config` for embedded basic auth credentials in remote origin URLs (`TG-GIT-002`).
3. **Mine Commit Log Diffs:** Inspect the last 50 commits (`git log -p`) for added tokens, keys, and credentials (`TG-GIT-001`).
4. **Audit Tracked Sensitive Files:** Ensure `.env`, private keys, and certificates are not tracked in git tree history (`TG-GIT-003`).
5. **Report & Revoke:** Provide immediate provider revocation steps and commit log cleanup guidance in `security_report.md`.
