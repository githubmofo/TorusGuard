# TG-SUPPLY-002: Vulnerable Dependency Review Missing

## Severity
High by default. Escalate to Critical when dependencies with known, weaponized remote code execution (RCE) or authentication bypass CVEs are identified.

## Applies To
- Node.js / JavaScript / TypeScript (`package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`)
- Python (`requirements.txt`, `pyproject.toml`, `Pipfile.lock`, `poetry.lock`)

## Why It Matters
Using third-party open-source packages with known security vulnerabilities exposes production web applications to automated supply-chain exploits, supply-chain poisoning, prototype pollution, cross-site scripting (XSS), and arbitrary code execution.

However, **automated bulk repair commands like `npm audit fix --force` introduce severe supply-chain regression hazards**:
- `npm audit fix --force` blindly upgrades packages across **major breaking version jumps** (e.g., Express 4 $\rightarrow$ 5, MongoDB Driver v2 $\rightarrow$ v6, Webpack 4 $\rightarrow$ 5).
- These breaking API changes break production routing, change database connection options, and crash running services.
- Remediation must be deliberate, selective, and verified through regression suites.

## What TorusGuard Looks For
1. Unpinned dependency versions or wildcards (`*`, `latest`) in manifests.
2. Missing automated vulnerability auditing steps (`npm audit`, `pip-audit`) in CI/CD workflows.
3. Automated fix scripts executing blind `--force` flags without test gates.
4. Dependencies flagged with CVEs exceeding acceptable severity thresholds.

## Unsafe Example
```bash
# UNSAFE: Blind automated fix forcing breaking major version upgrades
npm audit fix --force
```

```json
// UNSAFE: package.json with floating wildcard versions
{
  "dependencies": {
    "express": "*",
    "jsonwebtoken": "^8.0.0"
  },
  "scripts": {
    "audit-fix": "npm audit fix --force"
  }
}
```

## Safe Example
```bash
# SAFE: Apply non-breaking minor and patch fixes only
npm audit fix

# For dependencies requiring major version bumps to patch CVEs:
# 1. Inspect breaking changes manually:
npm audit --json

# 2. Upgrade specific package selectively:
npm install jsonwebtoken@9.0.2

# 3. Execute regression test suite before merging:
npm test
```

```yaml
# SAFE: Continuous vulnerability scanning in CI workflow (.github/workflows/security.yml)
name: Dependency Security Audit
on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Node Dependency Audit
        run: npm audit --audit-level=high
      - name: Run Python Dependency Audit
        run: |
          pip install pip-audit
          pip-audit -r requirements.txt --strict
```

## Remediation
1. **Never use `--force` in CI or production maintenance scripts:** Restrict automated remediation to `npm audit fix` (non-breaking minor/patch updates).
2. **Selective Major Upgrades:** For vulnerabilities that require a major version jump, consult the upstream CHANGELOG, evaluate breaking API changes, and upgrade the single package explicitly.
3. **Pin Exact Versions or Use Lockfiles:** Commit reproducible lockfiles (`package-lock.json`, `poetry.lock`, `requirements.txt`) to source control.
4. **Automate in CI:** Integrate `npm audit` or `pip-audit` as a blocking pull request check for High and Critical severities.

## Verification
- Run `npm audit` or `pip-audit` to confirm zero High/Critical unhandled CVEs.
- Confirm all existing unit and integration tests pass after any dependency update.
- Verify that `package-lock.json` changes reflect only intended, targeted packages.

## False Positives and Exceptions
- Vulnerabilities located solely in development dependencies (`devDependencies`, e.g., local build tools, linters) that are never bundled into client or server production environments may be exempted with documented risk acceptance.

## Related Rules
- `TG-SUPPLY-001`: Pinned Dependency Version Missing
- `TG-SUPPLY-003`: Container Build Secret Persistence
- `TG-SEC-001`: Hardcoded Secrets in Manifests
