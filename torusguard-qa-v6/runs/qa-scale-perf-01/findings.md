# TorusGuard v6 Detailed Findings

### 🚨 [TG-DB-004] Tenant Query Issue 0

- **Stable Finding ID:** `TG-DB-ca267e777ee4`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 90/100 (Confirmed)
- **Location:** `apps/service_0/models/query_0.py:1-5`

#### Evidence
```python
Model.objects.filter(id=x)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Tenant Query Issue 0 in `apps/service_0/models/query_0.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-ca267e777ee4`

</details>

---

### 🚨 [TG-DB-004] Tenant Query Issue 1

- **Stable Finding ID:** `TG-DB-8728d15d9cc2`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 90/100 (Confirmed)
- **Location:** `apps/service_1/models/query_1.py:1-5`

#### Evidence
```python
Model.objects.filter(id=x)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Tenant Query Issue 1 in `apps/service_1/models/query_1.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-8728d15d9cc2`

</details>

---

### 🚨 [TG-DB-004] Tenant Query Issue 2

- **Stable Finding ID:** `TG-DB-66a81d19428b`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 90/100 (Confirmed)
- **Location:** `apps/service_2/models/query_2.py:1-5`

#### Evidence
```python
Model.objects.filter(id=x)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Tenant Query Issue 2 in `apps/service_2/models/query_2.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-66a81d19428b`

</details>

---

### 🚨 [TG-DB-004] Tenant Query Issue 3

- **Stable Finding ID:** `TG-DB-ff76b506e040`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 90/100 (Confirmed)
- **Location:** `apps/service_3/models/query_3.py:1-5`

#### Evidence
```python
Model.objects.filter(id=x)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Tenant Query Issue 3 in `apps/service_3/models/query_3.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-ff76b506e040`

</details>

---

### 🚨 [TG-DB-004] Tenant Query Issue 4

- **Stable Finding ID:** `TG-DB-47c54b649084`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 90/100 (Confirmed)
- **Location:** `apps/service_4/models/query_4.py:1-5`

#### Evidence
```python
Model.objects.filter(id=x)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Tenant Query Issue 4 in `apps/service_4/models/query_4.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-47c54b649084`

</details>

---
