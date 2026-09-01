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
| `v0.7.x` (`v0.7.0`) | ✅ Yes | Current active release line (Authorized Runtime Validation & Bounded Exploitability Confirmation) |
| `v0.6.x` | ✅ Yes | Governed Remediation, Minimal Patching & Targeted Recheck System |
| `v0.5.x` | ⚠️ Best effort | Legacy reporting, validation engine, and rule schemas |
| `< v0.5.0` | ❌ No | Deprecated |

---

## Authorized Runtime Validation & Safety Controls (v0.7.0)

TorusGuard v0.7.0 adds runtime validation controls ensuring no automated agent probes live systems without verified authorization:
1. **Target Authorization Gate (`core/authorization.py`):** Requires written permission or target ownership verification with whitelisted hosts, allowed path prefixes, and request limits. Rejects unauthorized requests with `AuthorizationError`.
2. **Safety Review Gates (`core/safety_gate.py`):** Categorizes requests into `Auto-Allowed`, `Approval Required`, and `Manual Only`, automatically blocking destructive or privileged actions (`/admin/delete`, `/system/shutdown`).
3. **Automated Secret Redaction (`core/runtime_evidence.py`):** Strips Bearer tokens, credentials, and API keys prior to persisting request/response evidence.

---

## Governed Remediation & Sensitive-Path Safety Controls

TorusGuard incorporates proactive defense mechanisms to prevent AI coding agents from introducing regressions or applying unsafe automated code modifications:

1. **Patch Policy Governance (`core/governance.py`):**
   - Strictly enforces limits on additions ($\le 35$ lines) and deletions ($\le 25$ lines) per file.
   - Prohibits sweeping boilerplate rewrites, unstructured comment replacements, and multi-file cross-service churn.

2. **Sensitive-Path Review Levels:**
   - **Authentication & JWT:** Files matching `auth`, `login`, `jwt`, `token`, `session`, `password`.
   - **Multi-Tenancy:** Files matching `tenant`, `tenant_id`, `organization_id`, `org_id`, `workspace_id`.
   - **Secrets & Cryptography:** Files matching `secret`, `api_key`, `private_key`, `crypto`, `hmac`.
   - **Storage & Uploads:** Files matching `upload`, `storage`, `filepath`, `save_file`.
   - **CI/CD Infrastructure:** `.github/workflows/`, `Dockerfile`, `compose.yaml`.
   - **Enforcement:** Diffs in sensitive contexts with $> 10$ line churn automatically escalate to `Mandatory Security Sign-Off` and block automated patch execution.

3. **Targeted Scoped Recheck Verification (`core/rechecker.py`):**
   - Automatically re-evaluates AST sinks and trust boundaries after code edits, requiring human intervention if any regression (`Regressed`) or incomplete remediation (`Needs Manual Review`) is detected.

4. **GitHub Code Scanning Interoperability (`core/sarif.py`):**
   - Emits standard OASIS SARIF v2.1.0 logs with `partialFingerprints` (`primaryLocationLineHash`) to guarantee deterministic alert tracking and eliminate duplicate alert noise across pull requests.

