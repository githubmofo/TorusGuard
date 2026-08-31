# TorusGuard v6 Detailed Findings

### 🚨 [TG-PLATFORM-003] Production Debug Mode Enabled

- **Stable Finding ID:** `TG-PLATFORM-2c5c8ccd7dc1`
- **Root-Cause Cluster:** `cluster-platform-003`
- **Severity:** Medium | **Priority:** Near-Term (P1)
- **Confidence:** 95/100 (Confirmed)
- **Location:** `app.py:1-1`

#### Evidence
```python
DEBUG = True
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-PLATFORM-003] Production Debug Mode Enabled in `app.py`

**Severity:** Medium | **Priority:** Near-Term (P1)

**Finding ID:** `TG-PLATFORM-2c5c8ccd7dc1`

</details>

---

### 🚨 [TG-SEC-001] Hardcoded Secret Key

- **Stable Finding ID:** `TG-SEC-e7e7b41b5c85`
- **Root-Cause Cluster:** `cluster-secrets`
- **Severity:** Critical | **Priority:** Near-Term (P1)
- **Confidence:** 98/100 (Confirmed)
- **Location:** `app.py:2-2`

#### Evidence
```python
SECRET_KEY = "sk_live_1234567890"
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-SEC-001] Hardcoded Secret Key in `app.py`

**Severity:** Critical | **Priority:** Near-Term (P1)

**Finding ID:** `TG-SEC-e7e7b41b5c85`

</details>

---
