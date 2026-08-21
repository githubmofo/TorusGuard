# SQLAlchemy Rule Verification Matrix (TorusGuard v0.4.0)

| Rule ID | Rule Title | Test Target File | Detection Check | Expected Result | Confidence |
|---|---|---|---|---|:---:|
| `TG-INPUT-003` | SQL Injection in text() | `queries.py` | `text(f"SELECT ... '{val}'")` | Flagged as SQL Injection | Confirmed |
| `TG-AUTH-007` | Query Scoping (IDOR) | `queries.py` | `SELECT ... WHERE id = :id` missing `user_id` | Flagged as IDOR Risk | Confirmed |
| `TG-AUTH-006` | Mass Assignment Update | `queries.py` | `.update(updates)` using raw user dictionary | Flagged as Mass Assignment Risk | Confirmed |
