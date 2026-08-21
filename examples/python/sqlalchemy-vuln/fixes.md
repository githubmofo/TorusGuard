# Remediation Mapping: SQLAlchemy Vulnerable -> Hardened

| Vulnerability | Rule ID | Vulnerable File | Hardened File | Security Control Applied |
|---|---|---|---|---|
| SQL Injection in text() | `TG-INPUT-003` | `queries.py` | `queries.py` | Named parameter binding (`:email`) |
| Unscoped Query (IDOR) | `TG-AUTH-007` | `queries.py` | `queries.py` | Filter by `user_id == current_user_id` |
| Bulk Update Mass Assignment | `TG-AUTH-006` | `queries.py` | `queries.py` | Explicit field dictionary allowlist |
