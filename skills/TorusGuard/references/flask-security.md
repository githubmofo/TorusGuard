# TorusGuard Skill Reference: Flask Security

> **Loaded When:** Project uses `flask` dependencies or imports.

---

## 🛡️ Key Inspection Areas & Rules

### 1. Secret Key & Cookie Configuration
* `TG-SEC-001`: Inspect `app.config['SECRET_KEY']`. Flag hardcoded string literals.
* `TG-PLATFORM-003`: Verify `app.debug = False` in production configs.

### 2. Authorization & Ownership (IDOR)
* `TG-AUTH-007`: In route handlers querying database models by route variables (e.g. `<int:id>`), verify that the query filters by `current_user.id`.

### 3. CSRF Protection
* `TG-CSRF-001`: Verify that cookie-authenticated web forms initialize `flask_wtf.CSRFProtect`.

### 4. File Uploads
* `TG-INPUT-004`: Ensure uploaded filenames are filtered using `secure_filename()` and validate against an extension whitelist.
