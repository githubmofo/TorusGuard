# Contributing to TorusGuard

Thank you for your interest in contributing to TorusGuard! TorusGuard is an open-source, Markdown-first security guidance framework for AI coding agents.

This guide outlines how to propose new security rules, add framework guides, report false positives, submit validation reports, and open pull requests.

---

## Code of Conduct

All contributors and maintainers are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please report any unacceptable behavior to the project maintainers.

---

## Ways to Contribute

You can contribute in several key areas:
1. **Report a Bug:** Report broken links, incorrect skill formatting, or tooling issues.
2. **Report a False Positive:** Help refine existing rules that trigger on safe code patterns.
3. **Propose a Security Rule:** Add new guardrails covering emerging attack vectors.
4. **Author a Platform/Framework Guide:** Write guides for new stacks (e.g., FastAPI, Django, Go, Rails).
5. **Add Validation Reports:** Validate TorusGuard rules against open-source test applications.
6. **Improve Documentation & Examples:** Enhance readability, code clarity, and educational value.

---

## Issue Intake Guidelines

Before opening an issue, please check existing [GitHub Issues](https://github.com/githubmofo/TorusGuard/issues) to avoid duplicates.

* **One concern per issue:** Please keep each issue focused on a single topic, bug, or rule proposal.
* **Use Issue Templates:** We provide structured templates under `.github/ISSUE_TEMPLATE/` for bug reports, false positives, rule proposals, and platform requests.
* **Security Vulnerabilities in TorusGuard:** Do **not** open public issues for security vulnerabilities in TorusGuard itself. Review [SECURITY.md](SECURITY.md) for private disclosure instructions.

---

## Proposing a New Security Rule

New rules must follow the established TorusGuard structure:

1. **Rule ID Format:** `TG-<CATEGORY>-<NUMBER>` (e.g., `TG-SSRF-005`, `TG-AUTH-008`).
2. **Required Sections in Rule File (`rules/<category>/TG-*.md`):**
   - **Title & Severity:** (`Critical`, `High`, `Medium`, `Low`, `Informational`).
   - **Applies To:** Target languages, frameworks, or architectural components.
   - **Why It Matters:** Clear, non-hyped explanation of the security risk and impact.
   - **Detection Guidance:** Specific patterns, AST cues, or grep terms to identify the issue.
   - **Unsafe Example:** Realistic code illustrating the vulnerability (fake data only).
   - **Safe Example:** Clean, recommended pattern resolving the vulnerability.
   - **Remediation Steps:** Step-by-step developer instructions.
   - **Verification:** Actionable test command or manual check confirming the fix.
   - **False Positives / Exceptions:** Edge cases where the pattern is safe.
   - **Related Rules:** Cross-references to related TorusGuard IDs.

---

## Adding Framework & Platform Guides

Guides in `guides/` provide actionable security configurations for specific tech stacks (e.g., `guides/react-vite-security.md`).

When adding a guide:
- Document framework-specific defaults, headers, authentication hooks, and ORM safe patterns.
- Cross-reference applicable TorusGuard rule IDs (`TG-...`).
- Provide concrete, copy-pasteable configuration examples.

---

## Writing or Updating Validation Reports

Validation reports live in `docs/validation/` and document local testing against open-source applications.

Every report must include:
1. **Scope:** Target repository name, commit hash, stack, and authorization.
2. **Environment:** Node.js/Python version, OS, package manager.
3. **Finding Classification:** Every finding must be labeled:
   - `Confirmed` (directly observed)
   - `Likely` (strong indicator, needs runtime check)
   - `Manual Review` (business/architectural decision)
   - `Informational` (hardening advice)
4. **Limits:** Explicit statement of what the test proved and what it did not prove.

---

## Pull Request Guidelines

### 1. Branching
Create a descriptive branch from `main`:
* `feat/new-rule-ssrf-dns` (for new features or rules)
* `fix/false-positive-cache` (for bug fixes or rule refinements)
* `docs/fastapi-hardening-guide` (for documentation and guides)

### 2. Commit Message Conventions
We follow [Conventional Commits](https://www.conventionalcommits.org/):
* `feat(rules): add TG-EDGE-001 serverless secret isolation rule`
* `fix(cache): refine false-positive guidance for TG-CACHE-001`
* `docs(readme): improve quickstart instructions`
* `test(validation): add FastAPI validation report`

### 3. PR Checklist
Before submitting:
- [ ] Only fake, non-functional credentials and placeholder URLs are used.
- [ ] No real secrets, private keys, or deployable attack payloads are included.
- [ ] Technical claims are accurate and avoid exaggerated claims ("unhackable", "100% secure").
- [ ] Markdown formatting is clean, valid, and all internal links resolve.
- [ ] Relevant catalog files (`rules/README.md`) and `CHANGELOG.md` are updated if applicable.
- [ ] Context budget constraint verified: any modified workflow or skill stays strictly within **1,000–1,500 tokens** (maximum 300 lines).
- [ ] All 11 verification test suites pass cleanly:
  ```bash
  python harness/validate_v0_9_2_dual_track.py
  python harness/validate_v0_9_2_diff_and_monorepo.py
  python harness/validate_v0_9_2_workflows_and_skills.py
  python .torusguard/scripts/manifest_builder.py --check
  python harness/validate_v0_9_1_installer.py
  python harness/validate_v0_9_0_skills.py
  python harness/runner.py
  python harness/validate_v0_7_0_runtime.py
  python harness/validate_v0_8_0_part1.py
  python harness/validate_v0_8_0_part2.py
  python harness/validate_v0_8_0_part3.py
  ```
