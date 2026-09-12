# TG-SUPPLY-004: Unpinned CI Action

## Severity
Critical. Referencing third-party GitHub Actions using mutable branch or version tags (e.g. `uses: actions/checkout@v4`) allows attackers who compromise the action's repository to push malicious code that runs with your workflow's permissions.

## Applies To
- GitHub Actions Workflows (`.github/workflows/*.yml`)
- CI/CD Configurations

## Why It Matters
Git tags in third-party repositories are mutable pointers. An attacker who compromises a popular action maintainer's account can force-push a malicious commit to `@v3` or `@v4`, granting them immediate execution inside your CI environment with access to your repository secrets.

## What TorusGuard Looks For
- GitHub Actions `uses:` declarations referencing version tags (`@v4`, `@main`) instead of 40-character immutable commit SHA hashes.

## Unsafe Example
```yaml
# UNSAFE: Mutable tag vulnerable to tag spoofing
steps:
  - uses: actions/checkout@v4
  - uses: some-vendor/setup-tool@v1
```

## Safe Example
```yaml
# SAFE: Immutable commit SHA pinning with version comment
steps:
  - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
  - uses: some-vendor/setup-tool@c2e8c2f1f8b172a5a54db5e6b12a818c1b2c3d4e # v1.2.0
```

## Ponytail Remediation Budget
- Additions: <= 2 lines
- Deletions: <= 2 lines

## Remediation
1. Pin all external GitHub Actions to full 40-character commit SHAs.
2. Use tools like Dependabot or Renovate to automate SHA updates with release verification.

## Related Rules
- `TG-SUPPLY-003`: Unsafe CI/CD Secret Exposure
- `TG-SUPPLY-005`: Unsafe Dependency Install Script
