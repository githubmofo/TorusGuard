# TG-CACHE-003: Sensitive Data in URL Query Parameters

## Severity
Medium. Passing API keys, session tokens, passwords, or PII in URL query parameters causes secrets to be persisted in browser histories, web server access logs, and HTTP `Referer` headers.

## Applies To
- Authentication Flows, Invitation Links, Reset Handlers
- Frontend JS, Express, Django, FastAPI, Go, PHP

## Why It Matters
URLs are routinely logged in plaintext by reverse proxies, load balancers, CDN providers, and browser histories. If tokens are in query strings (`/login?token=xyz`), any external asset loaded on the page receives the token in the `Referer` header.

## What TorusGuard Looks For
- Query parameter patterns matching `api_key=`, `token=`, `secret=`, or `password=` in GET routes.

## Unsafe Example
```javascript
// UNSAFE: Accepting credentials or tokens in URL query string
app.get('/api/auth/callback', (req, res) => {
  const { apiKey, password } = req.query;
  authenticate(apiKey, password);
});
```

## Safe Example
```javascript
// SAFE: Passing credentials in Authorization header or POST request body
app.post('/api/auth/token', (req, res) => {
  const { apiKey, password } = req.body;
  authenticate(apiKey, password);
});
```

## Ponytail Remediation Budget
- Additions: <= 6 lines
- Deletions: <= 3 lines

## Remediation
1. Migrate authentication parameters to `Authorization: Bearer` headers or JSON request bodies via POST.
2. Strip sensitive query parameters from URLs using history replace state before page render.

## Related Rules
- `TG-SEC-001`: Hardcoded Secret or API Key in Tracked Source
- `TG-SEC-004`: Sensitive Information in Logs
