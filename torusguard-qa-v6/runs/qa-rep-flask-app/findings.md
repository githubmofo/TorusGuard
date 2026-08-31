# TorusGuard v6 Detailed Findings

### 🚨 [TG-INPUT-005] Server-Side Template Injection (SSTI)

- **Stable Finding ID:** `TG-INPUT-67344b2cf839`
- **Root-Cause Cluster:** `cluster-template-escaping`
- **Severity:** Critical | **Priority:** Near-Term (P1)
- **Confidence:** 96/100 (Confirmed)
- **Location:** `app.py:10-10`

#### Evidence
```python
return render_template_string(f"Hello {name}")
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-INPUT-005] Server-Side Template Injection (SSTI) in `app.py`

**Severity:** Critical | **Priority:** Near-Term (P1)

**Finding ID:** `TG-INPUT-67344b2cf839`

</details>

---

### 🚨 [TG-INPUT-006] Unsafe File Path Traversal

- **Stable Finding ID:** `TG-INPUT-a1f3d99b3c7b`
- **Root-Cause Cluster:** `cluster-path-traversal`
- **Severity:** High | **Priority:** Near-Term (P1)
- **Confidence:** 93/100 (Confirmed)
- **Location:** `app.py:16-16`

#### Evidence
```python
f.save(os.path.join("/var/uploads", f.filename))
```

<details><summary><b>🎫 Ticket Payload</b></summary>

**Issue:** [TG-INPUT-006] Unsafe File Path Traversal in `app.py`

**Severity:** High | **Priority:** Near-Term (P1)

**Finding ID:** `TG-INPUT-a1f3d99b3c7b`

</details>

---
