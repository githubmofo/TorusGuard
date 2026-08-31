# TorusGuard v6 Detailed Findings

### 🚨 [TG-DB-004] Missing Tenant Query Scoping in Billing

- **Stable Finding ID:** `TG-DB-123197ca71b1`
- **Root-Cause Cluster:** `cluster-tenant-isolation`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 85/100 (High Confidence)
- **Location:** `apps/django_core/billing/views.py:42-42`

#### Evidence
```python
Invoice.objects.get(id=inv_id)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-DB-004] Missing Tenant Query Scoping in Billing in `apps/django_core/billing/views.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-DB-123197ca71b1`

</details>

---

### 🚨 [TG-SSRF-001] Unvalidated Outbound Destination in Ingestion Service

- **Stable Finding ID:** `TG-SSRF-f0ee17e7f427`
- **Root-Cause Cluster:** `cluster-ssrf-network`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 85/100 (High Confidence)
- **Location:** `apps/fastapi_service/routes/fetcher.py:18-18`

#### Evidence
```python
httpx.get(target_url)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-SSRF-001] Unvalidated Outbound Destination in Ingestion Service in `apps/fastapi_service/routes/fetcher.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-SSRF-f0ee17e7f427`

</details>

---

### 🚨 [TG-WEBHOOK-001] Missing Webhook HMAC Verification

- **Stable Finding ID:** `TG-WEBHOOK-c8d8bc1ce13f`
- **Root-Cause Cluster:** `cluster-webhook-auth`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 85/100 (High Confidence)
- **Location:** `apps/flask_webhook/handler.py:12-12`

#### Evidence
```python
payload = request.json
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-WEBHOOK-001] Missing Webhook HMAC Verification in `apps/flask_webhook/handler.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-WEBHOOK-c8d8bc1ce13f`

</details>

---

### 🚨 [TG-INPUT-006] Path Traversal in Deep Analytics Worker

- **Stable Finding ID:** `TG-INPUT-e72b59b0206e`
- **Root-Cause Cluster:** `cluster-path-traversal`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 85/100 (High Confidence)
- **Location:** `services/core/v1/subsystems/analytics/processors/workers/storage.py:88-88`

#### Evidence
```python
open(os.path.join(DIR, filename), 'wb')
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-INPUT-006] Path Traversal in Deep Analytics Worker in `services/core/v1/subsystems/analytics/processors/workers/storage.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-INPUT-e72b59b0206e`

</details>

---

### 🚨 [TG-SUPPLY-001] Unpinned GitHub Action in Production Pipeline

- **Stable Finding ID:** `TG-SUPPLY-2bf5cfd0f6b9`
- **Root-Cause Cluster:** `cluster-supply-001`
- **Severity:** Medium | **Priority:** Near-Term (P1)
- **Confidence:** 85/100 (High Confidence)
- **Location:** `infra/.github/workflows/deploy.yml:15-15`

#### Evidence
```python
uses: actions/checkout@v2
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-SUPPLY-001] Unpinned GitHub Action in Production Pipeline in `infra/.github/workflows/deploy.yml`

**Severity:** Medium | **Priority:** Near-Term (P1)

**Finding ID:** `TG-SUPPLY-2bf5cfd0f6b9`

</details>

---
