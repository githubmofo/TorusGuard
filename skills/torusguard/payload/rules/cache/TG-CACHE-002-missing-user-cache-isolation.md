# TG-CACHE-002: Missing User Cache Isolation

## Severity
High. Storing per-user computed assets or database query results in shared application memory caches (Redis, Memcached) without tenant or user ID scoping leads to cross-user data leakage.

## Applies To
- Application Caching Layers (Redis, Memcached, LRU Caches)
- Node.js, Python, Go, Java

## Why It Matters
If cache keys are formed using generic keys (e.g., `cache:dashboard_summary`) rather than tenant-qualified keys (`cache:tenant_{tid}:user_{uid}:dashboard_summary`), the first user to query the dashboard caches their data, and all subsequent users receive that cached data.

## What TorusGuard Looks For
- Cache get/set calls where the cache key lacks user or tenant identifier variables.

## Unsafe Example
```python
# UNSAFE: Generic cache key shared across all users
@app.get("/api/dashboard")
def get_dashboard(user: User = Depends(get_current_user)):
    data = cache.get("dashboard_data")
    if not data:
        data = generate_dashboard(user.id)
        cache.set("dashboard_data", data, expire=300)
    return data
```

## Safe Example
```python
# SAFE: Fully isolated cache key scoped by tenant and user
@app.get("/api/dashboard")
def get_dashboard(user: User = Depends(get_current_user)):
    cache_key = f"dashboard:tenant_{user.tenant_id}:user_{user.id}"
    data = cache.get(cache_key)
    if not data:
        data = generate_dashboard(user.id)
        cache.set(cache_key, data, expire=300)
    return data
```

## Ponytail Remediation Budget
- Additions: <= 6 lines
- Deletions: <= 3 lines

## Remediation
1. Always prefix cache keys with organizational and user identifiers.
2. Clear tenant cache keys immediately upon logout or permissions change.

## Related Rules
- `TG-DB-004`: Missing Multi-Tenant Query Isolation
- `TG-CACHE-001`: Sensitive Response Publicly Cacheable
