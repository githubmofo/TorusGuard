# TorusGuard v6 Detailed Findings

### 🚨 [TG-DB-004] Missing Multi-Tenant Query Scoping

- **Stable Finding ID:** `TG-DB-298a6a4002d2`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 92/100 (Confirmed)
- **Location:** `views.py:6-6`

#### Evidence
```python
invoice = Invoice.objects.get(id=invoice_id)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Missing Multi-Tenant Query Scoping in `views.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-298a6a4002d2`

</details>

---

### 🚨 [TG-INPUT-005] Disabled Template Autoescaping via mark_safe

- **Stable Finding ID:** `TG-INPUT-7dd18dc1ab8a`
- **Root-Cause Cluster:** `cluster-template-escaping`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 90/100 (Confirmed)
- **Location:** `views.py:8-8`

#### Evidence
```python
rendered = mark_safe(f"<h1>{invoice.title}</h1>")
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-INPUT-005] Disabled Template Autoescaping via mark_safe in `views.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-INPUT-7dd18dc1ab8a`

</details>

---
