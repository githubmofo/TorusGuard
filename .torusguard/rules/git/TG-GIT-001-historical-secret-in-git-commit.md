# TG-GIT-001: Historical Secret Leaked in Git Commit History

## Severity
Critical. Committing a secret permanently writes it to the repository's immutable DAG history. Even if deleted in a later commit, anyone with clone access can extract the secret.

## Applies To
- Git Commit Objects, Commit Diff Logs (`git log -p`), Packfiles
- All source files and configuration commits

## Why It Matters
Git is an append-only, content-addressable storage system. A commit removing a secret (`git rm .env`) only adds a new tree state; the secret blob remains forever reachable in previous commit objects, reflogs, and packfile deltas.

## What TorusGuard Looks For
1. High-entropy credentials, private keys, or API tokens committed in historical git commits (`git log -p -S`).
2. Deleted secrets that still reside in historical tree objects.

## Unsafe Example
```bash
# UNSAFE: Secret committed to repository history
git commit -m "Add stripe integration with live key sk_live_abc123"
# Later "fix" that leaves the historical commit intact:
git rm config/stripe.json && git commit -m "Remove secret"
```

## Safe Example
```bash
# SAFE: Secrets stored in untracked environment files (.env)
# Added to .gitignore before first commit
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Ignore environment secrets"
```

## Remediation
1. Immediately **revoke and rotate** the leaked credential at the provider.
2. Purge the secret from history using `git-filter-repo` or BFG Repo-Cleaner:
   ```bash
   git filter-repo --invert-paths --path config/stripe.json
   ```
3. Force-push to all remote branches and advise all team members to re-clone.

## Related Rules
- `TG-SEC-001`: Hardcoded Secrets
- `TG-GIT-002`: Plaintext Credentials in Git Config
