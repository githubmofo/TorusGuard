# Contributing to TorusGuard

Thank you for helping make AI-built web applications safer. This guide explains how to contribute security rules, fixes, and examples.

## Ways to Contribute

1. **Propose a new security rule** — Open an issue using the "Security Rule Proposal" template.
2. **Report a false positive** — Open an issue using the "False Positive Report" template.
3. **Improve reference modules** — Submit a PR editing files under `skills/torusguard/references/`.
4. **Add stack-specific examples** — Extend examples or add new demo apps with before/after documentation.
5. **Fix documentation** — Clarify wording, add detection patterns, or improve remediation steps.

## Development Setup

```bash
git clone https://github.com/githubmofo/TorusGuard.git
cd TorusGuard
npm run validate
npm run check-examples
```

## Pull Request Guidelines

1. **One concern per PR** — Keep changes focused (one module, one rule, or one example fix).
2. **Include before/after code** — Every new hard ban needs a vulnerable example and a safe alternative.
3. **No real secrets** — Use placeholders like `YOUR_JWT_SECRET`, never real credentials.
4. **Run validation** — Ensure `npm run validate` passes before submitting.
5. **Update CHANGELOG.md** — Add an entry under `[Unreleased]` for user-visible changes.

## Security Rule Format

When proposing a rule, include:

| Field | Description |
|-------|-------------|
| **ID** | Proposed ID (e.g., `TG-042`) |
| **Title** | Short name |
| **Severity** | Critical, High, Medium, Low, Informational |
| **Category** | One of the seven modules |
| **Detection** | What to search for in code |
| **Hard ban** | Yes/No |
| **Remediation** | Concrete fix with code example |
| **False positives** | When this rule should not apply |

## Module Structure

Each reference file in `skills/torusguard/references/` should contain:

- Scope
- Threat model
- Detection patterns
- Hard bans
- Required safe defaults
- Framework-specific examples
- Verification checklist
- False-positive guidance

## Example Apps

The `examples/` directory contains intentionally vulnerable and hardened demo apps. When adding vulnerabilities to the vulnerable app:

- Mark each with a comment: `// TORUSGUARD-DEMO: TG-xxx description`
- Link the vulnerability to the relevant reference module in README
- Ensure the hardened app demonstrates the fix

## Code of Conduct

Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Be respectful and constructive.

## Questions

Open a GitHub Discussion or issue if you are unsure whether a change fits the project scope.
