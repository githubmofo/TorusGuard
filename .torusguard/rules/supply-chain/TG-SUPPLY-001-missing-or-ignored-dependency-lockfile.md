# TG-SUPPLY-001: Missing or Ignored Dependency Lockfile

## Severity
High. Omitting or `.gitignore`-ing dependency lockfiles (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `Poetry.lock`, `Cargo.lock`, `go.sum`) allows non-deterministic builds and exposes installations to malicious sub-dependency updates.

## Applies To
- npm, pnpm, yarn, pip, poetry, cargo, go
- All polyglot projects

## Why It Matters
Without a committed lockfile, running `npm install` or `pip install` resolves the latest compatible semantic version (`^1.0.0`). If a third-party dependency author account is compromised and publishes a malicious patch version, your CI/CD pipeline installs it automatically.

## What TorusGuard Looks For
- `.gitignore` files containing `package-lock.json`, `yarn.lock`, or `pnpm-lock.yaml`.
- Repositories with manifest files (`package.json`) lacking corresponding lockfiles.

## Unsafe Example
```gitignore
# UNSAFE: Ignoring dependency lockfiles in version control
node_modules/
package-lock.json
yarn.lock
```

## Safe Example
```gitignore
# SAFE: Tracking lockfiles in version control; ignoring only node_modules
node_modules/
dist/
build/
```

## Ponytail Remediation Budget
- Additions: <= 1 line
- Deletions: <= 2 lines

## Remediation
1. Remove lockfile references from `.gitignore`.
2. Run `npm install` to generate `package-lock.json` and commit it to git.
3. In CI/CD pipelines, use `npm ci` or `pnpm install --frozen-lockfile` instead of `npm install`.

## Related Rules
- `TG-SUPPLY-002`: Vulnerable Dependency Review Missing
- `TG-SUPPLY-004`: Unpinned CI Action
