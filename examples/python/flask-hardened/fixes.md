# Hardened Fixes Matrix: Flask

| Risk | Rule ID | Hardened Implementation |
|---|---|---|
| Hardcoded Secret Key | `TG-SEC-001` | `app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')` |
| Document View IDOR | `TG-AUTH-007` | Verifies `doc.owner_id == session['user_id']` |
| Unsafe File Upload | `TG-INPUT-004` | `secure_filename()` with extension allowlist and storage boundary |
| Missing CSRF Protection | `TG-CSRF-001` | Initialized `CSRFProtect(app)` |
