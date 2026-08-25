# Security Policy

## Reporting Security Vulnerabilities

The TorusGuard project takes security seriously. If you believe you have discovered a vulnerability or security flaw in **TorusGuard itself** (such as unsafe skill instructions, template flaws, or repository infrastructure), please report it responsibly and privately.

**Do not file public GitHub issues, discussions, or pull requests for undisclosed security vulnerabilities.**

---

## What Belongs in a Security Report?

| Belongs in Private Security Disclosure | Belongs in Public GitHub Issues |
|---|---|
| 🔒 Flaws in TorusGuard skill instructions that cause unsafe code generation | 💡 Requesting a new security rule (`TG-...`) |
| 🔒 Insecure defaults in `templates/` or `guides/` | 🐛 Reporting a false positive or minor rule detection bug |
| 🔒 Credential leaks or malicious dependencies in the TorusGuard repository | ❓ General usage questions, installation help, or feature ideas |

> **Note on Third-Party Applications & Educational Fixtures:**  
> - **External Codebases:** TorusGuard is an open-source guidance framework. If you find a security vulnerability in an application audited with TorusGuard, please report it directly to the maintainers of that application following their private disclosure policy.  
> - **Educational Fixtures:** Files located in `examples/vulnerable-*/`, `examples/python/*-vuln/`, and `tests/fixtures/*/` are **intentionally vulnerable educational fixtures**. They are deliberately insecure by design for validation purposes and must never be deployed to production.

---

## How to Submit a Private Report

1. **Preferred Method:** Use [GitHub Private Vulnerability Reporting](https://github.com/githubmofo/TorusGuard/security/advisories/new).
2. **Alternative Method:** Contact the project maintainer directly via GitHub ([@githubmofo](https://github.com/githubmofo) / Jenish Lad).

### What to Include in Your Report
Please provide:
- A clear description of the issue.
- Affected files, guides, templates, or rule identifiers.
- Step-by-step reproduction instructions or code snippet.
- Assessment of potential security impact.
- Any suggested remediations or mitigations.

---

## Response Commitments & Triage Targets

* **Initial Acknowledgment / Triage:** Within **48 to 72 hours**.
* **Status Update & Remediation Plan:** Within **7 days** of initial triage.
* **Coordinated Disclosure:** We adhere to standard coordinated disclosure principles. Once a fix is verified and released, a public security advisory will be published crediting the researcher (unless anonymity is requested).

---

## Authorized Testing & Legal Boundaries

In alignment with OWASP and NIST vulnerability disclosure guidelines:
- Security testing against TorusGuard must be non-destructive and limited to repository source code, templates, and portable skill definitions.
- Probing or scanning live infrastructure, production accounts, or external services is strictly out of scope.

---

## Supported Versions

Security updates and patches are prioritized for the current active release line:

| Version Line | Supported? | Status |
|---|:---:|---|
| `v0.5.x` | ✅ Yes | Current active release line (Architecture & Workflow Release) |
| `v0.4.x` | ⚠️ Best effort | Critical security fixes only |
| `< v0.4.0` | ❌ No | Deprecated |
