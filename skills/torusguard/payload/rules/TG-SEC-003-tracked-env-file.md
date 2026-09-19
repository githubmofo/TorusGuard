# TG-SEC-003: Tracked Environment File

## Severity
High

## Applies To
- Git repositories containing `.env`, `.env.local`, `.env.production`, or similar files
- Application backends, frontend builds, deployment scripts, and tooling
- Monorepos with per-package environment files
- Any tracked path where secrets can be stored in plain text

## Why It Matters
Environment files are commonly used to store credentials, tokens, and connection strings.  
When tracked by git, these values propagate to every clone, fork, mirror, and CI artifact.  
Even if a file is later deleted, prior commits may retain sensitive data unless history is remediated.

## What TorusGuard Looks For
- `.env*` files present in tracked source control history or current index
- Environment files committed outside approved template patterns
- Presence of sensitive key names in tracked env files:
  - `*_SECRET`, `*_TOKEN`, `*_PASSWORD`, `DATABASE_URL`, `SERVICE_ROLE_KEY`
- Mismatch between `.gitignore` policy and tracked env artifacts
- Commits that introduce plaintext operational credentials

## Unsafe Example
```bash
# git status --short
A  .env
M  src/config.ts
```

```env
# .env
DATABASE_URL=postgres://report_user:R3portProdPass@db:5432/reports
JWT_SECRET=invoice_signing_secret_2026
REDIS_PASSWORD=cache_password_11
```

## Safe Example
```gitignore
# .gitignore
.env
.env.*
!.env.example
```

```env
# .env.example
DATABASE_URL=
JWT_SECRET=
REDIS_PASSWORD=
```

## Remediation (numbered)
1. Remove tracked `.env*` files from git index while preserving local copies.
2. Add strict ignore rules for environment files in repository root and subprojects.
3. Replace committed env files with sanitized `.env.example` templates.
4. Rotate all credentials that existed in tracked environment files.
5. Audit commit history to determine exposure scope and retention obligations.
6. If required, perform approved history rewrite and coordinate downstream cleanup.
7. Enforce pre-commit and CI checks that block tracked secret-bearing env files.

## Verification
- Run git status and confirm `.env*` files are untracked (except approved templates).
- Check `.gitignore` patterns include root and nested environment file variants.
- Validate deployed systems use secure environment injection, not committed files.
- Confirm rotated values are active and old credentials are invalid.
- Review pull requests for accidental reintroduction of tracked env files.

## False Positives and Exceptions
- `.env.example` and `.env.template` are acceptable if they contain no real secrets.
- Test fixtures may include fake credentials only when clearly non-operational.
- Some repos intentionally track non-sensitive env files; exceptions need approval.
- Emergency temporary commits are still violations unless formally exempted.

## Related Rules
- [TG-SEC-001](./TG-SEC-001-hardcoded-secrets.md) - Hardcoded secrets in source files
- [TG-SEC-002](./TG-SEC-002-public-environment-secrets.md) - Secrets exposed through public env prefixes
- [TG-SEC-004](./TG-SEC-004-sensitive-logging.md) - Runtime leakage through sensitive logging
