def get_unscoped_order(session, order_id: int):
    # VULNERABLE: Unscoped query
    return {"order_id": order_id, "scoped": False}
