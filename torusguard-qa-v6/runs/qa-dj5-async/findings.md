# TorusGuard v6 Detailed Findings

### 🚨 [TG-DB-004] Async Missing Multi-Tenant Query Scoping

- **Stable Finding ID:** `TG-DB-025151f79600`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 95/100 (Confirmed)
- **Location:** `views.py:8-8`

#### Evidence
```python
invoice = await Invoice.objects.aget(id=invoice_id)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Async Missing Multi-Tenant Query Scoping in `views.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-025151f79600`

</details>

---
