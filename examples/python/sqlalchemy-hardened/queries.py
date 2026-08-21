from sqlalchemy import text

# ✅ TG-INPUT-003: Parameterized text() query
def find_user(session, email: str):
    query = text("SELECT * FROM users WHERE email = :email")
    return session.execute(query, {"email": email}).fetchall()

# ✅ TG-AUTH-007: Ownership-filtered query (IDOR safe)
def get_order(session, order_id: int, current_user_id: int):
    query = text("SELECT * FROM orders WHERE id = :id AND user_id = :user_id")
    return session.execute(query, {"id": order_id, "user_id": current_user_id}).fetchone()

ALLOWED_UPDATE_FIELDS = {'bio', 'display_name'}

# ✅ TG-AUTH-006: Whitelist-filtered update
def update_user_fields(session, user_id: int, updates: dict):
    filtered = {k: v for k, v in updates.items() if k in ALLOWED_UPDATE_FIELDS}
    set_clause = ", ".join(f"{k} = :{k}" for k in filtered.keys())
    if not set_clause:
        return
    query = text(f"UPDATE users SET {set_clause} WHERE id = :user_id")
    filtered["user_id"] = user_id
    session.execute(query, filtered)
