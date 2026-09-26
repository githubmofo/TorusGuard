# TG-GIT-003: Sensitive Tracked File in .gitignore Violation

## Severity
High. Sensitive files (`.env`, private keys, keystores) tracked in git index despite matching `.gitignore` patterns can accidentally leak private credentials on the next commit or push.

## Applies To
- Git Index (`git ls-files`), `.gitignore`, Repository Root

## Why It Matters
Adding a file to `.gitignore` does **not** un-track it if it was previously staged or committed. Git continues to track changes to the file, and changes will be committed and pushed to remote servers unless explicitly removed with `git rm --cached`.

## What TorusGuard Looks For
1. Tracked files matching common secret filenames: `.env`, `.env.local`, `*.pem`, `id_rsa`, `*.p12`, `*.key`.
2. Files listed in `.gitignore` that still appear in `git ls-files`.

## Unsafe Example
```bash
# UNSAFE: .env is in .gitignore, but still tracked in git
git ls-files | grep .env
# Output: .env.production
```

## Safe Example
```bash
# SAFE: Remove from git tracking while keeping the file on disk
git rm --cached .env.production
git commit -m "Untrack .env.production"
```

## Remediation
1. Untrack the file without deleting local contents:
   ```bash
   git rm --cached <sensitive-file>
   git commit -m "Untrack sensitive configuration file"
   ```
2. Verify `.gitignore` contains the pattern.

## Related Rules
- `TG-SEC-003`: Tracked Env File
- `TG-GIT-001`: Historical Secret Leaked in Git Commit History
