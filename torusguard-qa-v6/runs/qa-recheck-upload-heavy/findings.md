# TorusGuard v6 Detailed Findings

### 🚨 [TG-INPUT-006] Path Traversal in Storage Handler

- **Stable Finding ID:** `TG-INPUT-7c848b1baf09`
- **Root-Cause Cluster:** `cluster-path-traversal`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 96/100 (Confirmed)
- **Location:** `storage.py:6-6`

#### Evidence
```python
dest = os.path.join(UPLOAD_DIR, raw_filename)
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-INPUT-006] Path Traversal in Storage Handler in `storage.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-INPUT-7c848b1baf09`

</details>

---
