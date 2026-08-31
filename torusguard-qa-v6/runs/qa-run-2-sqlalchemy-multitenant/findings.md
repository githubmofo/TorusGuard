# TorusGuard v6 Detailed Findings

### 🚨 [TG-DB-004] Missing Tenant Query Isolation in SQLAlchemy

- **Stable Finding ID:** `TG-DB-bc6be5e7a8d0`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 95/100 (Confirmed)
- **Location:** `queries.py:5-5`

#### Evidence
```python
return db.query(Account).filter(Account.id == account_id).first()
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Missing Tenant Query Isolation in SQLAlchemy in `queries.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-bc6be5e7a8d0`

</details>

---
