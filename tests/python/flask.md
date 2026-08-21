# Flask Rule Verification Matrix (TorusGuard v0.4.0)

| Rule ID | Rule Title | Test Target File | Detection Check | Expected Result | Confidence |
|---|---|---|---|---|:---:|
| `TG-SEC-001` | Hardcoded Secrets | `app.py` | `app.config['SECRET_KEY'] = 'hardcoded...'` | Flagged as Hardcoded Secret | Confirmed |
| `TG-AUTH-007` | Object Ownership IDOR | `app.py` | `/documents/<doc_id>` lookup without user ID check | Flagged as IDOR Risk | Confirmed |
| `TG-INPUT-004` | Unsafe File Upload | `app.py` | `file.save(os.path.join(..., file.filename))` | Flagged as Unsafe File Upload | Confirmed |
| `TG-CSRF-001` | Missing CSRF Protection | `app.py` | POST upload endpoint lacks CSRF token validation | Flagged as Missing CSRF | Confirmed |
