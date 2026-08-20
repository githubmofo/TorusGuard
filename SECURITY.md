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

> **Note on Third-Party Applications & Examples:**  
> - TorusGuard is an open-source guidance framework. If you find a security vulnerability in an application audited with TorusGuard, please report it directly to the maintainers of that application.  
> - Files located in `examples/vulnerable-*/` and `tests/fixtures/vulnerable/` are **intentionally vulnerable educational fixtures**. They are deliberately insecure by design and should never be deployed to production.

---

## How to Submit a Private Report

1. **Preferred Method:** Use [GitHub Private Vulnerability Reporting](https://github.com/githubmofo/TorusGuard/security/advisories/new).
2. **Alternative Method:** If GitHub Advisories is unavailable, contact the maintainer directly at:  
   `[Maintainer Security Contact: security@example.com / Jenish Lad via GitHub]` *(Maintainer: replace with dedicated email if applicable)*

### What to Include in Your Report
Please provide:
- A clear description of the issue.
- Affected files or rule identifiers.
- Step-by-step reproduction instructions or code snippet.
- Assessment of potential security impact.
- Any suggested remediations or mitigations.

---

## Response Commitments & Triage Targets

* **Initial Acknowledgment / Triage:** Within **48 to 72 hours**.
* **Status Update & Remediation Plan:** Within **7 days** of initial triage.
* **Coordinated Disclosure:** We follow coordinated disclosure principles. Once a fix is verified and released, a public security advisory will be published crediting the researcher (unless anonymity is requested).

---

## Supported Versions

Security updates are prioritized for the current active release line:

| Version Line | Supported? | Status |
|---|:---:|---|
| `v0.3.x` | ✅ Yes | Current active release |
| `v0.2.x` | ⚠️ Best effort | Critical fixes only |
| `< v0.2.0` | ❌ No | Deprecated |
