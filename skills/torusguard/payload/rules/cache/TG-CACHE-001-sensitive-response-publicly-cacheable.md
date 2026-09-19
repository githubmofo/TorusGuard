# TG-CACHE-001: Sensitive Response Publicly Cacheable

## Severity
High. Serving authenticated personal data, financial records, or credentials without private `Cache-Control` headers allows shared intermediary proxy servers and CDNs to cache and leak sensitive records to other users.

## Applies To
- Authenticated Endpoints, User Profiles, Billing Dashboards
- Express, Next.js, FastAPI, Django, Flask, Rails, Spring

## Why It Matters
When endpoints returning PII omit cache control directives, shared corporate proxies or public edge CDNs may cache the response. Subsequent requests from other users on the same proxy can receive the cached personal data of the initial requester.

## What TorusGuard Looks For
- Routes returning user profiles, tokens, or private data with `Cache-Control: public` or missing `Cache-Control` entirely.

## Unsafe Example
```javascript
// UNSAFE: Missing cache control or explicitly public caching on private data
app.get('/api/user/profile', authMiddleware, (req, res) => {
  res.set('Cache-Control', 'public, max-age=3600');
  res.json(req.user);
});
```

## Safe Example
```javascript
// SAFE: Explicit private no-store cache control on sensitive responses
app.get('/api/user/profile', authMiddleware, (req, res) => {
  res.set('Cache-Control', 'no-store, no-cache, must-revalidate, private');
  res.set('Pragma', 'no-cache');
  res.json(req.user);
});
```

## Ponytail Remediation Budget
- Additions: <= 4 lines
- Deletions: <= 2 lines

## Remediation
1. Inject global middleware setting `Cache-Control: no-store, private` on all authenticated API responses.
2. Verify reverse proxies and CDNs do not cache responses containing `Authorization` or `Cookie` headers.

## Related Rules
- `TG-CACHE-002`: Missing User Cache Isolation
- `TG-PLATFORM-002`: Missing Security Headers
