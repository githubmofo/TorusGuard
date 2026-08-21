# Regression Fixture: Missing Tenant Scoping in SQLAlchemy

- **Framework:** SQLAlchemy
- **Target Rule:** `TG-AUTH-007`
- **Expected Classification:** `Confirmed`
- **Expected Rule IDs:** `TG-AUTH-007`
- **Reasoning:** Query looks up record by primary key `filter(Order.id == order_id)` without scoping to the authenticated tenant/user ID (`Order.user_id == current_user.id`).

## Sample Code
```python
def get_order_details(session, order_id: int):
    # VULNERABLE: Direct primary key query without tenant boundary
    return session.query(Order).filter(Order.id == order_id).first()
```
