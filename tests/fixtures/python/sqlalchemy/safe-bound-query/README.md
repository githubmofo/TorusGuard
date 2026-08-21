# Regression Fixture: Safe Bound Parameter Query in SQLAlchemy

- **Framework:** SQLAlchemy
- **Target Rule:** `TG-INPUT-003`
- **Expected Classification:** Safe (No findings)
- **Expected Rule IDs:** None / Safe
- **Reasoning:** Raw `text()` query uses named bound parameter `:search_term` with wildcard value supplied inside dictionary parameter mapping.

## Sample Code
```python
from sqlalchemy import text

def search_products(session, user_query: str):
    stmt = text("SELECT * FROM products WHERE name LIKE :pattern")
    return session.execute(stmt, {"pattern": f"%{user_query}%"}).fetchall()
```
