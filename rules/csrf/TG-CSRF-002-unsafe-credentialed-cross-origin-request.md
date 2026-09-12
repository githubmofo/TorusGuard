# TG-CSRF-002: Unsafe Credentialed Cross-Origin Requests

## Severity
Critical. Enabling credentialed cross-origin access (`credentials: true` / `Access-Control-Allow-Credentials: true`) combined with dynamic reflection of incoming `Origin` headers allows any untrusted domain to read authenticated responses.

## Applies To
- CORS Middleware Configurations
- Express (cors), FastAPI, Flask-CORS, Django-cors-headers, Spring Security

## Why It Matters
When a server blindly reflects the `Origin` header while allowing credentials, any malicious site visited by an authenticated user can make cross-origin requests and read private user data, completely circumventing the Same-Origin Policy.

## What TorusGuard Looks For
- CORS configurations reflecting `req.headers.origin` directly when `credentials: true` is enabled.

## Unsafe Example
```javascript
// UNSAFE: Blindly reflecting any origin with credentials enabled
app.use(cors({
  origin: (origin, callback) => callback(null, true),
  credentials: true
}));
```

## Safe Example
```javascript
// SAFE: Strictly validating origin against an explicit environment allowlist
const allowedOrigins = (process.env.ALLOWED_ORIGINS || 'https://app.example.com').split(',');
app.use(cors({
  origin: (origin, callback) => {
    if (!origin || allowedOrigins.includes(origin)) return callback(null, true);
    callback(new Error('Blocked by CORS'));
  },
  credentials: true
}));
```

## Ponytail Remediation Budget
- Additions: <= 8 lines
- Deletions: <= 4 lines

## Remediation
1. Restrict CORS origins to a static, verified allowlist stored in environment variables.
2. Never reflect untrusted `req.headers.origin` when credentials are permitted.

## Related Rules
- `TG-PLATFORM-001`: Wildcard CORS With Credentials
- `TG-CSRF-001`: Missing CSRF Protection
