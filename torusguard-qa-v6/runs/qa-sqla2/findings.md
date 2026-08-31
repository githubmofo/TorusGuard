# TorusGuard v6 Detailed Findings

### 🚨 [TG-DB-004] Missing Tenant Predicate in SQLAlchemy 2.0 select()

- **Stable Finding ID:** `TG-DB-0ce0fbe73c53`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 96/100 (Confirmed)
- **Location:** `queries.py:7-7`

#### Evidence
```python
stmt = select(Account).where(Account.id == account_id)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Missing Tenant Predicate in SQLAlchemy 2.0 select() in `queries.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-0ce0fbe73c53`

</details>

---
