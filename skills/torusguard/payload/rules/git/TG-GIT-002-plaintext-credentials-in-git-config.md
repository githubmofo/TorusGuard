# TG-GIT-002: Plaintext Credentials in Git Config

## Severity
High. Embedding plaintext usernames, passwords, or personal access tokens in `.git/config` remote URLs exposes credentials in local logs and backup snapshots.

## Applies To
- `.git/config`, `~/.gitconfig`, Git remote definitions

## Why It Matters
When developers embed personal access tokens directly into git remote URLs (e.g. `https://username:ghp_secret@github.com/repo.git`), the credential is saved in clear text in `.git/config`. Any process, script, or extension with local filesystem access can read the token.

## What TorusGuard Looks For
1. Remote URL strings matching `https?://[^:]+:[^@]+@`.
2. Hardcoded Personal Access Tokens (PATs) embedded in `.git/config` or checkout scripts.

## Unsafe Example
```ini
# UNSAFE: Plaintext token stored in .git/config
[remote "origin"]
    url = https://developer:ghp_1234567890abcdef1234567890abcdef@github.com/org/repo.git
    fetch = +refs/heads/*:refs/remotes/origin/*
```

## Safe Example
```ini
# SAFE: Use Git Credential Helper or SSH keys
[remote "origin"]
    url = git@github.com:org/repo.git
    fetch = +refs/heads/*:refs/remotes/origin/*
```

## Remediation
1. Strip embedded passwords from the remote URL:
   ```bash
   git remote set-url origin https://github.com/org/repo.git
   ```
2. Configure a secure Git credential helper (`git credential-manager` or `osxkeychain` / `wincred`) or switch to SSH key authentication.

## Related Rules
- `TG-GIT-001`: Historical Secret Leaked in Git Commit History
- `TG-SEC-001`: Hardcoded Secrets
