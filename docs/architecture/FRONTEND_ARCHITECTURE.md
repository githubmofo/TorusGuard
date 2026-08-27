# TorusGuard Frontend Security & Presentation Architecture

## 1. Overview
The Frontend Architecture document defines TorusGuard's dual relationship with client-side code:
1. **Frontend Security Rules:** Guardrails governing client-side web application architectures (React, Next.js, Vite, Vue, Svelte).
2. **Human-First Presentation Standards:** Presentation architecture used by TorusGuard to render clean, readable, and actionable security reports in Markdown and CLI terminals.

---

## 2. The Browser-Code Truth Principle

> **Core Axiom:** If client software receives an artifact, the end-user has uninhibited inspection and modification access to that artifact via browser Developer Tools, network interceptors, or local memory debuggers.

TorusGuard enforces strict frontend boundary rules:
- **`TG-CLIENT-001` (Production Source Maps):** Prevents deployment of unminified `.map` files that expose private business logic and backend route schemas to the public internet.
- **`TG-CLIENT-002` (Sensitive Bundle Content):** Audits frontend build bundles (Vite `dist/`, Next.js `.next/`) to ensure private API keys, payment secret tokens, or internal database URLs are never bundled into client bundles.
- **`TG-DB-001` (Direct Client Database Access):** Forbids client-side JavaScript from executing direct database queries with privileged database credentials.

---

## 3. Human-First Report Presentation Architecture

TorusGuard formats all outputs into standardized, highly structured Markdown cards designed for seamless collaboration between non-technical stakeholders and security engineers.

### 3.1. Standard Finding Card Layout
```markdown
### 🚨 [TG-AUTH-008] Untrusted Role or Tenant Header Injection

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **Priority** | Immediate (P0) |
| **Confidence** | 92/100 (Confirmed) |
| **Target File** | `backend/api/auth.py:L42-48` |

#### 💼 Business Impact
Attackers can elevate privileges to administrator by crafting custom `X-User-Role` headers, leading to total tenant data compromise.

#### 🔧 Technical Mechanics
The endpoint reads `request.headers.get("X-User-Role")` directly without cryptographic signature or gateway verification.

#### 📝 Evidence
```python
# backend/api/auth.py:42
user_role = request.headers.get("X-User-Role", "user")
```

#### 🛠️ Recommended Remediation (FastAPI)
```python
# Extract role from cryptographically verified token claims
async def get_current_user_roles(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
    return payload.get("roles", [])
```
```

---

## 4. Ticket-Ready Issue Tracker Payloads
Every finding card includes an expandable `<details>` section containing pre-formatted Markdown ready to copy-paste directly into Jira, GitHub Issues, or Linear tickets.
