# TG-SEC-005: Secret or Private Key in Git History

## Severity
Critical. Committing private API keys, credentials, or private certificates into git history persists them permanently across all cloned repositories, even if deleted in subsequent commits.

## Applies To
- Git Repositories, Public and Private Remotes
- All Languages & Frameworks

## Why It Matters
Deleting a secret file in a follow-up commit (`git rm .env`) does NOT remove it from git history. Attackers clone public repositories and run scanners (`git log -p`) to extract historical secrets within seconds.

## What TorusGuard Looks For
- Git commit objects or patch diffs containing private keys, AWS access keys, or JWT secret strings.

## Unsafe Example
```bash
# UNSAFE: Adding .env with live credentials directly to git tracking
git add .env
git commit -m "Add production database credentials"
```

## Safe Example
```bash
# SAFE: Keeping .env in .gitignore; using .env.example with placeholder tokens
echo ".env" >> .gitignore
git add .gitignore .env.example
git commit -m "Add environment configuration baseline"
```

## Ponytail Remediation Budget
- Additions: <= 2 lines
- Deletions: <= 2 lines

## Remediation
1. Immediately rotate any secret that was committed to git history.
2. Use tools like `git-filter-repo` or BFG Repo-Cleaner to purge the commit blob from repository history.
3. Add `.env` and `*.pem` to `.gitignore`.

## Related Rules
- `TG-SEC-001`: Hardcoded Secret or API Key in Tracked Source
- `TG-SEC-003`: Unencrypted Secret in Tracked Config File
