def execute_safe_query(session, term: str):
    # SAFE: Named parameters
    query = "SELECT * FROM products WHERE name LIKE :pattern"
    params = {"pattern": f"%{term}%"}
    return {"query": query, "params": params}
