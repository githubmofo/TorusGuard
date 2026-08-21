# TorusGuard v0.4.0 Validation Report: Flask

> **Target:** Flask Reference Application (`examples/python/flask-vuln/`)  
> **Framework:** Flask 3.0+ / Werkzeug  
> **Test Mode:** Local Simulated `/torusguard audit` & `/torusguard harden`  
> **Status:** Validation Completed Successfully  

---

## 🎯 1. Test Scope & Purpose
Validate TorusGuard rules for Flask applications, checking secret key initialization, route ownership, file upload handling, and CSRF token defenses.

---

## 🔍 2. Verified Findings

### 🔴 1. Hardcoded Secret Key (`TG-SEC-001`)
* **Classification:** `Confirmed`
* **Evidence:** `app.py` sets `app.config['SECRET_KEY'] = 'hardcoded_insecure_development_key'`.
* **Impact:** Enables session forgery and tamper vulnerabilities.
* **Remediation:** Load from environment variable with mandatory production guard.

### 🔴 2. Missing Ownership Verification in Document Route (`TG-AUTH-007`)
* **Classification:** `Confirmed`
* **Evidence:** `/documents/<int:doc_id>` returns document objects without matching `owner_id == session['user_id']`.
* **Impact:** Cross-user data leakage by guessing integer IDs.
* **Remediation:** Enforce session user ownership check.

### 🟠 3. Unsafe File Upload Processing (`TG-INPUT-004`)
* **Classification:** `Confirmed`
* **Evidence:** File upload saves raw client-provided `file.filename` directly to disk.
* **Impact:** Path traversal and file overwrite attacks (e.g. `../../etc/passwd`).
* **Remediation:** Sanitize with `werkzeug.utils.secure_filename` and check extension against an allowlist.

### 🟠 4. Missing CSRF Defense (`TG-CSRF-001`)
* **Classification:** `Confirmed`
* **Evidence:** Application uses cookie-based state changes without `flask_wtf.CSRFProtect`.
* **Impact:** Susceptible to cross-site request forgery.
* **Remediation:** Initialize `CSRFProtect(app)`.

---

## ⚖️ 3. Validation Limitations
- Local testing fixture only; server WSGI configurations (e.g., Gunicorn worker timeouts and Nginx proxy headers) require deployment environment review.
