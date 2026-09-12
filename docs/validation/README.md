# TorusGuard Validation Suite

This directory contains formal, reproducible validation records documenting how TorusGuard rules perform across diverse application architectures, frameworks, and programming languages as of **v1.3.5**.

---

## 🎯 Why Validation Matters

TorusGuard is a security guidance framework, autonomous remediation engine, and runtime validation system for AI coding agents. To ensure that its rules produce accurate, actionable findings rather than noisy hallucinations, every supported stack undergoes local repository validation.

### What Validation Proves
1. **Rule Applicability:** Verifies that all 74 rules across 18 families accurately identify genuine vulnerability patterns.
2. **Framework Independence:** Proves that TorusGuard's threat model applies across 16+ programming languages (Go, Rust, Java, C#, PHP, Ruby, Kotlin, Elixir, Dart, C/C++, Python, TypeScript/JavaScript) and 30+ frameworks.
3. **Living Security Report Accuracy:** Guarantees that finding state transitions in `security_report.md` are synchronized, mathematically verified, and deterministic.
4. **Ponytail Boundary Compliance:** Asserts that candidate patches strictly adhere to line churn budgets ($\le 35$ additions, $\le 25$ deletions).

### What Validation Does NOT Prove
- Validation is **not** an offensive penetration test of target applications.
- Validation does **not** probe unauthorized production infrastructure.
- Educational fixtures are intentionally insecure by design and must never be deployed to production.

---

## 📁 Validation Reports Index

### 🧪 1. Comprehensive Master & Release Validation Reports
- **Master Automated Test Battery:** `npm test` (`python harness/runner.py`) — **81/81 Test Suites Passing**
- **v1.3.0 Polyglot Engine Suite:** `harness/validate_v1_3_0_polyglot.py` (10 assertions, 100% pass)
- **v1.2.0 AI IDE Rules & HTML Reporter Suite:** `harness/validate_v1_2_0_rules_and_html.py` (8 assertions, 100% pass)
- **v1.1.0 Advanced Memory & Governance Suite:** `harness/validate_v1_1_0_advanced_memory.py` (9 assertions, 100% pass)
- **v1.0.0 Core Security Memory Suite:** `harness/validate_v1_0_0_memory.py` (11 assertions, 100% pass)
- **v0.9.2 Diff Guard & Monorepo Engine Suite:** `harness/validate_v0_9_2_diff_and_monorepo.py`
- **v0.9.2 Workflows & Skills Suite:** `harness/validate_v0_9_2_workflows_and_skills.py` (35 assertions, 100% pass)
- **v0.9.1 Autonomous Installer Sandbox Simulation:** `harness/validate_v0_9_1_installer.py` (14 assertions, 100% pass)
- **v0.9.0 Granular Skills Validation Suite:** `harness/validate_v0_9_0_skills.py` (53 assertions, 100% pass)
- **v0.7.0 Senior QA Runtime Validation Suite:** `harness/validate_v0_7_0_runtime.py` (67 assertions, 100% pass)
- [Enterprise Multi-Repository Portfolio Evaluation (26 Repositories)](portfolio-evaluation-report.md)
- [v0.5.6 Large-Project Validation Portfolio Report (10 Repositories)](v0.5.6-large-project-validation-report.md)
- [Complete Historical & Version Validation Report](complete-version-validation.md)
- [v0.4.1 Real-World Validation Report](v0.4.1-real-world-validation.md)
- [Authorized Repository Validation Template & Protocol](authorized-repo-validation-template.md)
- [Cross-Platform Rule Parity Report](cross-platform-rule-parity.md)

### 🧪 2. Framework Reference Fixture Reports
| Target Application / Framework | Language & Stack | Primary Rules Validated | Validation Report Link |
|---|---|---|---|
| **OWASP NodeGoat** | Node.js, Express, MongoDB | CSRF (`TG-CSRF-001`), Cache Security (`TG-CACHE-001`), Dependency Supply Chain (`TG-SUPPLY-*`) | [nodegoat-v0.3.0-validation.md](nodegoat-v0.3.0-validation.md) |
| **Django Reference App** | Python, Django 4.2 LTS | Secret management (`TG-SEC-001`), IDOR (`TG-AUTH-007`), ModelForm Mass Assignment (`TG-AUTH-006`), Cache (`TG-CACHE-001`) | [django-v0.4.0-validation.md](django-v0.4.0-validation.md) |
| **DRF API Reference** | Python, Django REST Framework | ViewSet Queryset Scoping (`TG-AUTH-007`), Serializer Fields (`TG-AUTH-006`), Throttling (`TG-RATE-001`), Pagination (`TG-RATE-002`) | [drf-v0.4.0-validation.md](drf-v0.4.0-validation.md) |
| **FastAPI Test Target** | Python, FastAPI, Pydantic | SSRF (`TG-SSRF-001`), Webhook Signatures (`TG-WEBHOOK-001`), Schema Validation (`TG-AUTH-006`) | [fastapi-v0.4.0-validation.md](fastapi-v0.4.0-validation.md) |
| **Flask Reference App** | Python, Flask, Werkzeug | Secret keys (`TG-SEC-001`), IDOR (`TG-AUTH-007`), Uploads (`TG-INPUT-004`), CSRF (`TG-CSRF-001`) | [flask-v0.4.0-validation.md](flask-v0.4.0-validation.md) |

### 🏢 3. Real-World Authorized Code Review Records
- [Real-World Validation Program Overview](real-world/README.md)
- [Django + DRF SaaS Validation Record](real-world/django-drf-real-world.md)
- [FastAPI Webhook Gateway Validation Record](real-world/fastapi-real-world.md)
- [Flask Document Portal Validation Record](real-world/flask-sqlalchemy-real-world.md)
- [Polyglot Monorepo Validation Record](real-world/mixed-stack-real-world.md)
