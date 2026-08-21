# Flask Security Research Notes (TorusGuard v0.4.0)

## Research Findings
- **Minimal Core Architecture:** Unlike Django, Flask does not include built-in CSRF protection by default; `Flask-WTF` (`CSRFProtect`) is required for browser cookie-authenticated state changes.
- **Session Security Defaults:** `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY`, and `SESSION_COOKIE_SAMESITE` must be set explicitly.
- **Upload Safety:** Werkzeug's `secure_filename()` must be paired with extension allowlists to avoid path traversal.
