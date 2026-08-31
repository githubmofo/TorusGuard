# TorusGuard v6 Detailed Findings

### 🚨 [TG-SUPPLY-001] Unpinned GitHub Action and Unbounded Permissions

- **Stable Finding ID:** `TG-SUPPLY-9dcb428a6a5c`
- **Root-Cause Cluster:** `cluster-supply-001`
- **Severity:** Medium | **Priority:** Near-Term (P1)
- **Confidence:** 90/100 (Confirmed)
- **Location:** `.github/workflows/ci.yml:6-6`

#### Evidence
```python
uses: actions/checkout@v2
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-SUPPLY-001] Unpinned GitHub Action and Unbounded Permissions in `.github/workflows/ci.yml`

**Severity:** Medium | **Priority:** Near-Term (P1)

**Finding ID:** `TG-SUPPLY-9dcb428a6a5c`

</details>

---
