from sqlalchemy import text

# ❌ TG-INPUT-003: String interpolation inside raw text()
def find_user(session, email: str):
    query = text(f"SELECT * FROM users WHERE email = '{email}'")
    return session.execute(query).fetchall()

# ❌ TG-AUTH-007: Unscoped order query (IDOR)
def get_order(session, order_id: int):
    # Simulated query missing user_id filter
    query = text(f"SELECT * FROM orders WHERE id = {order_id}")
    return session.execute(query).fetchone()

# ❌ TG-AUTH-006: Unfiltered mass assignment update
def update_user_fields(session, user_id: int, updates: dict):
    # Passes client dict directly into DB update
    query = text(f"UPDATE users SET {','.join(f'{k}={v}' for k,v in updates.items())} WHERE id = {user_id}")
    session.execute(query)
