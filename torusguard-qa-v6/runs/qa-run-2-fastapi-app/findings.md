# TorusGuard v6 Detailed Findings

### 🚨 [TG-SSRF-001] Unvalidated Outbound HTTP Request (SSRF)

- **Stable Finding ID:** `TG-SSRF-8f0db4e58390`
- **Root-Cause Cluster:** `cluster-ssrf-network`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 94/100 (Confirmed)
- **Location:** `main.py:9-9`

#### Evidence
```python
res = await client.get(url)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-SSRF-001] Unvalidated Outbound HTTP Request (SSRF) in `main.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-SSRF-8f0db4e58390`

</details>

---

### 🚨 [TG-AUTH-008] Untrusted Role Header Injection

- **Stable Finding ID:** `TG-AUTH-25179ed066c6`
- **Root-Cause Cluster:** `cluster-header-trust`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 90/100 (Confirmed)
- **Location:** `main.py:14-14`

#### Evidence
```python
if x_user_role != "admin":
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-AUTH-008] Untrusted Role Header Injection in `main.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-AUTH-25179ed066c6`

</details>

---
