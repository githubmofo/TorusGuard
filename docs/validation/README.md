# TorusGuard Validation Suite

This directory contains formal, reproducible validation records documenting how TorusGuard rules perform against real-world and test application architectures.

---

## 🎯 Why Validation Matters

TorusGuard is a security guidance framework for AI coding agents. To ensure that its rules produce accurate, actionable findings rather than noisy hallucinations, every major version undergoes local repository validation.

### What Validation Proves
1. **Rule Applicability:** Verifies that rules accurately identify genuine vulnerability patterns (e.g., missing CSRF protection, exposed sensitive response caching, unvalidated webhooks).
2. **Framework Independence:** Proves that TorusGuard's threat model applies across diverse runtime environments (e.g., Node.js/Express, Python/FastAPI).
3. **Evidence-Confidence Accuracy:** Ensures that issues requiring human context (e.g., business logic workflows, database RLS) are correctly classified as `Manual Review` rather than false `Confirmed` vulnerabilities.

### What Validation Does NOT Prove
- Validation is **not** a penetration test of the target applications.
- Validation does **not** prove that every TorusGuard rule is guaranteed to detect 100% of flaws in every framework.
- Validation on educational repositories (like NodeGoat) does not guarantee that third-party package managers can automatically resolve breaking dependency upgrades (`npm audit fix --force`).

---

## 📁 Validation Reports

| Target Application | Stack | Primary Rules Validated | Report Link |
|---|---|---|---|
| **OWASP NodeGoat** | Node.js, Express, MongoDB | CSRF (`TG-CSRF-001`), Cache Security (`TG-CACHE-001`), Dependency Supply Chain (`TG-SUPPLY-*`), SSRF & Business Logic Review | [nodegoat-v0.3.0-validation.md](nodegoat-v0.3.0-validation.md) |
| **FastAPI Test Target** | Python, FastAPI, Pydantic | SSRF (`TG-SSRF-001`), Webhook Signatures (`TG-WEBHOOK-001`), Mass Assignment (`TG-AUTH-006`) | [fastapi-v0.3.0-validation.md](fastapi-v0.3.0-validation.md) |

---

## 🔍 Finding Classification Standard

Every validated finding is classified into one of four confidence categories:

* **`Confirmed`:** Directly observed in source code or configuration (e.g., missing CSRF token verification middleware in an active POST route).
* **`Likely`:** Strong static indicators exist, but runtime or deployment environment configuration should be confirmed.
* **`Manual Review`:** Requires business intent or architectural knowledge that static code analysis cannot deduce (e.g., whether an unauthenticated webhook endpoint has upstream proxy authentication).
* **`Informational`:** Hardening recommendations and defensive coding best practices.

---

## 🤝 Adding a New Validation Report
We welcome validation reports for new stacks (Django, Go, Rails, Next.js App Router). Please review [CONTRIBUTING.md](../../CONTRIBUTING.md) and use the structure established in existing validation reports.
