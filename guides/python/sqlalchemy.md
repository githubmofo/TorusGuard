# SQLAlchemy Security Guide (TorusGuard v0.4.0)

> **Scope:** Data-layer security guidance for Python applications using SQLAlchemy (ORM & Core). Covers parameterized query construction, `text()` bindings, tenant query scoping, bulk update mass assignment, session lifecycle, and transaction isolation.

---

## 🔍 1. Parameterized Queries & `text()` (`TG-INPUT-003`)

SQLAlchemy ORM query methods (`filter()`, `filter_by()`) parameterize queries automatically. However, using raw SQL clauses with `text()` requires explicit parameter binding.

### ❌ Unsafe Pattern: String Interpolation with `text()`
```python
# VULNERABLE: Direct f-string interpolation into raw SQL
from sqlalchemy import text

def find_user_by_email(session, email: str):
    query = text(f"SELECT * FROM users WHERE email = '{email}'")  # ❌ SQL Injection
    return session.execute(query).fetchall()
```

### ✅ Safe Pattern: Parameterized Binding
```python
# SAFE: Named parameter binding
from sqlalchemy import text

def find_user_by_email(session, email: str):
    query = text("SELECT * FROM users WHERE email = :email")  # ✅ Parameterized
    return session.execute(query, {"email": email}).fetchall()
```

---

## 👤 2. Query Scoping & Multi-Tenant Authorization (`TG-AUTH-007`)

An ORM query is not secure if it omits tenant or user boundaries.

### ❌ Unsafe Pattern
```python
# VULNERABLE: Any caller can access any order by ID
def get_order(session, order_id: int):
    return session.query(Order).filter(Order.id == order_id).first()
```

### ✅ Safe Pattern
```python
# SAFE: Scope query strictly to the current tenant / user
def get_order(session, order_id: int, current_user_id: int):
    return session.query(Order).filter(
        Order.id == order_id, 
        Order.user_id == current_user_id
    ).first()
```

---

## 📝 3. Bulk Updates & Mass Assignment (`TG-AUTH-006`)

Avoid passing raw dictionary payloads into `.update()`.

### ❌ Unsafe Pattern
```python
# VULNERABLE: Accepts arbitrary dict fields directly into update
def update_profile(session, user_id: int, client_data: dict):
    session.query(User).filter(User.id == user_id).update(client_data)
```

### ✅ Safe Pattern
```python
# SAFE: Explicit column whitelist
ALLOWED_FIELDS = {'bio', 'display_name', 'phone_number'}

def update_profile(session, user_id: int, client_data: dict):
    sanitized_updates = {k: v for k, v in client_data.items() if k in ALLOWED_FIELDS}
    session.query(User).filter(User.id == user_id).update(sanitized_updates)
```

---

## 🔄 4. Transaction Boundaries & Session Lifecycle

* Always manage session lifecycles using context managers (`with Session() as session:` or FastAPI dependencies) to ensure sessions and connections are closed.
* Ensure failed operations roll back cleanly to avoid leaving database connections in aborted transaction states.

---

## 📋 Manual Review Checklist for SQLAlchemy

- [ ] All `text()` constructs use `:param` bindings rather than f-strings or `.format()`.
- [ ] Multi-tenant queries include tenant/user ID filter conditions.
- [ ] Bulk `.update()` queries validate and whitelist editable fields.
- [ ] Sessions are scoped to request lifecycles and close cleanly upon completion.
- [ ] Connection pool sizes and timeouts are configured to prevent connection pool exhaustion.
