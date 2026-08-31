# TorusGuard v6 Detailed Findings

### 🚨 [TG-SEC-001] Secret Exposed in Dockerfile Layer

- **Stable Finding ID:** `TG-SEC-42a69f48e90a`
- **Root-Cause Cluster:** `cluster-secrets`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 98/100 (Confirmed)
- **Location:** `Dockerfile:5-5`

#### Evidence
```python
ENV DATABASE_PASSWORD="secret_in_docker"
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-SEC-001] Secret Exposed in Dockerfile Layer in `Dockerfile`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-SEC-42a69f48e90a`

</details>

---
