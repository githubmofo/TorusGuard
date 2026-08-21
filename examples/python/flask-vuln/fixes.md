# Remediation Mapping: Flask Vulnerable -> Hardened

| Vulnerability | Rule ID | Vulnerable File | Hardened File | Security Control Applied |
|---|---|---|---|---|
| Hardcoded Secret Key | `TG-SEC-001` | `app.py` | `app.py` | Load secret from `os.environ.get("FLASK_SECRET_KEY")` |
| Document View IDOR | `TG-AUTH-007` | `app.py` | `app.py` | Scope query to `user_id = current_user.id` |
| Missing CSRF Defense | `TG-CSRF-001` | `app.py` | `app.py` | Initialize `CSRFProtect(app)` |
| Unsafe Upload Filename | `TG-INPUT-004` | `app.py` | `app.py` | Sanitize with `secure_filename()` & extension whitelist |
