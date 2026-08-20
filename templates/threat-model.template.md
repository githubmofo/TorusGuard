# 🛡️ Project Threat Model - [PROJECT_NAME]

> **Overview:** Security context, trust boundaries, and high-risk scenarios for `[PROJECT_NAME]`.  
> **Last Updated:** [DATE] • **Status:** Active

---

## 🏗️ 1. Architecture & Boundaries

```text
[Browser / Client]  -->  (Public API Routes)  -->  [Backend Server]  -->  [Database / Storage]
     (Untrusted)               (Boundary 1)           (Trusted)            (Boundary 2)
```

* **Frontend:** [React / Next.js / Vite / etc.]
* **Backend:** [Node.js / Express / Python / etc.]
* **Database / Services:** [PostgreSQL / Supabase / Firebase / MongoDB / Redis]
* **External APIs:** [Stripe / GitHub OAuth / Cloud Storage / Webhooks]

---

## 💎 2. Critical Assets to Protect

| Asset | Why It's Critical | Primary Protection |
|---|---|---|
| 🔑 **Secrets & API Keys** | Database passwords, payment signing keys | Server-side `.env` (never in client bundles) |
| 👤 **User Private Data** | PII, profile data, billing info | Server-side authorization & ownership checks |
| 🛡️ **Admin Capabilities** | User management, balance adjustments | Strict role verification on server APIs |

---

## ⚠️ 3. Key Threat Scenarios & Mitigations

### 1. Unauthorized Data Access (IDOR)
* **Risk:** User A accesses User B's records by changing IDs in the request URL.
* **Defense:** Every database query must filter by the authenticated session user ID (`WHERE user_id = req.user.id`).

### 2. Privilege Escalation (Mass Assignment)
* **Risk:** Attacker sends `{ isAdmin: true }` in profile updates.
* **Defense:** Whitelist only allowed fields before passing input to the database.

### 3. Server-Side Request Forgery (SSRF)
* **Risk:** Server fetches arbitrary URLs provided by users and accesses internal cloud metadata.
* **Defense:** Validate protocols (http/https only), resolve DNS, and block private IP ranges (`10.x`, `192.168.x`, `169.254.x`).

---

## 📋 4. Security Checklist for Developers

- [ ] All database queries and admin actions happen on trusted server-side code.
- [ ] No `NEXT_PUBLIC_*` or `VITE_*` environment variables contain secret keys.
- [ ] Rate limiting is enabled on public endpoints (login, register, search).
- [ ] CORS is restricted to approved production domains.
