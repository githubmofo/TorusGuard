# TorusGuard Validation Suite

This directory contains formal, reproducible validation records documenting how TorusGuard rules perform across diverse application architectures and programming languages.

---

## 🎯 Why Validation Matters

TorusGuard is a security guidance framework for AI coding agents. To ensure that its rules produce accurate, actionable findings rather than noisy hallucinations, every supported stack undergoes local repository validation.

### What Validation Proves
1. **Rule Applicability:** Verifies that rules accurately identify genuine vulnerability patterns (e.g., missing CSRF protection, mass assignment, IDOR, unvalidated webhooks).
2. **Framework Independence:** Proves that TorusGuard's threat model applies across diverse runtime environments (Node.js/Express, Django, DRF, FastAPI, Flask).
3. **Evidence-Confidence Accuracy:** Ensures that issues requiring human context (e.g., business logic workflows, database RLS) are correctly classified as `Manual Review` rather than false `Confirmed` vulnerabilities.

### What Validation Does NOT Prove
- Validation is **not** a penetration test of the target applications.
- Validation does **not** prove that every TorusGuard rule is guaranteed to detect 100% of flaws in every custom framework setup.
- Validation on educational repositories does not guarantee that third-party package managers can automatically resolve breaking dependency upgrades without human code review.

---

## 📁 Validation Reports Index

| Target Application / Framework | Language & Stack | Primary Rules Validated | Validation Report Link |
|---|---|---|---|
| **OWASP NodeGoat** | Node.js, Express, MongoDB | CSRF (`TG-CSRF-001`), Cache Security (`TG-CACHE-001`), Dependency Supply Chain (`TG-SUPPLY-*`) | [nodegoat-v0.3.0-validation.md](nodegoat-v0.3.0-validation.md) |
| **Django Reference App** | Python, Django 4.2 LTS | Secret management (`TG-SEC-001`), IDOR (`TG-AUTH-007`), ModelForm Mass Assignment (`TG-AUTH-006`), Cache (`TG-CACHE-001`) | [django-v0.4.0-validation.md](django-v0.4.0-validation.md) |
| **DRF API Reference** | Python, Django REST Framework | ViewSet Queryset Scoping (`TG-AUTH-007`), Serializer Fields (`TG-AUTH-006`), Throttling (`TG-RATE-001`), Pagination (`TG-RATE-002`) | [drf-v0.4.0-validation.md](drf-v0.4.0-validation.md) |
| **FastAPI Test Target** | Python, FastAPI, Pydantic | SSRF (`TG-SSRF-001`), Webhook Signatures (`TG-WEBHOOK-001`), Schema Validation (`TG-AUTH-006`) | [fastapi-v0.4.0-validation.md](fastapi-v0.4.0-validation.md) |
| **Flask Reference App** | Python, Flask, Werkzeug | Secret keys (`TG-SEC-001`), IDOR (`TG-AUTH-007`), Uploads (`TG-INPUT-004`), CSRF (`TG-CSRF-001`) | [flask-v0.4.0-validation.md](flask-v0.4.0-validation.md) |
| **Cross-Platform Parity** | Node.js & Python Ecosystems | Parity comparison across 6 universal rule categories | [cross-platform-rule-parity.md](cross-platform-rule-parity.md) |

---

## 🔍 Finding Classification Standard

Every validated finding is classified into one of four confidence categories:

* **`Confirmed`:** Directly observed in source code or configuration (e.g., hardcoded secret, missing CSRF token middleware).
* **`Likely`:** Strong static indicators exist, but runtime or deployment environment configuration should be confirmed.
* **`Manual Review`:** Requires business intent or architectural knowledge that static code analysis cannot deduce (e.g., whether an unauthenticated webhook endpoint has upstream proxy authentication).
* **`Informational`:** Hardening recommendations and defensive coding best practices.
