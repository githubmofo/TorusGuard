# Hardened Fixes Matrix: SQLAlchemy

| Risk | Rule ID | Hardened Implementation |
|---|---|---|
| SQL Injection in text() | `TG-INPUT-003` | `text("SELECT * FROM users WHERE email = :email")` with param dict |
| IDOR in Order Query | `TG-AUTH-007` | `text("SELECT * FROM orders WHERE id = :id AND user_id = :user_id")` |
| Mass Assignment Update | `TG-AUTH-006` | Whitelist dictionary filtering (`ALLOWED_FIELDS`) |
