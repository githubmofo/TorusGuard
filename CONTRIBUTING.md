# Contributing to TorusGuard

TorusGuard is a Markdown-first agent skill — not an npm package. Contributions are documentation, rules, examples, and guides.

## Ways to contribute

1. **Propose a security rule** — use the [rule proposal template](.github/ISSUE_TEMPLATE/rule_proposal.md)
2. **Report a false positive** — use the [false positive template](.github/ISSUE_TEMPLATE/false_positive.md)
3. **Improve an existing rule** — use the [rule improvement template](.github/ISSUE_TEMPLATE/security_rule_improvement.md)
4. **Submit a PR** — edit rules, references, guides, templates, or examples

## Development setup

```bash
git clone https://github.com/githubmofo/TorusGuard.git
cd TorusGuard
# No npm install required — review Markdown locally
```

## Pull request guidelines

1. One concern per PR
2. Every new rule needs: ID proposal, rationale, severity, unsafe example, safe example, detection, remediation, verification, false positives
3. No real secrets — placeholders only
4. Update `rules/README.md` and relevant reference module
5. Update `CHANGELOG.md` under `[Unreleased]` for user-visible changes

## New rule requirements

Every proposed rule must include:

| Field | Required |
|-------|----------|
| Rule ID proposal | e.g., `TG-SEC-005` |
| Security rationale | Why it matters |
| Default severity | Critical / High / Medium / Low / Info |
| Unsafe example | Original, framework-appropriate |
| Safe example | Corrected pattern |
| Detection approach | What to search for |
| Remediation | Numbered steps |
| Verification steps | How to confirm fix |
| False positives / exceptions | When not to flag |
| Framework notes | Where relevant |
| Test/example impact | Which examples to update |

## Rule file format

Follow the section order in existing `rules/TG-*.md` files. Link related rules in **Related Rules**.

## Example apps

- Vulnerable examples must include `WARNING: intentionally vulnerable` in README
- Mark flaws with `// TG-RULE-ID` comments
- Hardened examples must demonstrate the fix
- All secrets must be fake and labeled non-functional

## Code of conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Security vulnerabilities in TorusGuard

Do **not** open public issues for security flaws in TorusGuard itself. See [SECURITY.md](SECURITY.md).
