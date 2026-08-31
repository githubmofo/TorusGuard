# TorusGuard v6 Detailed Findings

### 🚨 [TG-AUTH-007] Unauthenticated Server Action (Next.js 14)

- **Stable Finding ID:** `TG-AUTH-c32c06c4a7b4`
- **Root-Cause Cluster:** `cluster-idor-scoping`
- **Severity:** Critical | **Priority:** Near-Term (P1)
- **Confidence:** 95/100 (Confirmed)
- **Location:** `actions.ts:3-7`

#### Evidence
```python
await db.document.delete({ where: { id: docId } });
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-AUTH-007] Unauthenticated Server Action (Next.js 14) in `actions.ts`

**Severity:** Critical | **Priority:** Near-Term (P1)

**Finding ID:** `TG-AUTH-c32c06c4a7b4`

</details>

---
