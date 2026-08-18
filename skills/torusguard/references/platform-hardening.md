# Platform and HTTP Hardening

## Scope

Apply essential web-platform protections around headers, CORS, errors, uploads, dependencies, and production deployment.

## Threat Model

- Cross-origin attacks via misconfigured CORS
- Clickjacking via missing frame protection
- MIME sniffing attacks
- Information disclosure via verbose errors
- Dependency vulnerabilities
- Insecure production configuration (debug mode, HTTP)

## Detection Patterns

| Pattern | Severity |
|---------|----------|
| `Access-Control-Allow-Origin: *` with `credentials: true` | Critical |
| Production stack traces returned to users | High |
| Debug mode enabled in production | High |
| Missing body limits on public JSON endpoints | Medium |
| Raw database/provider errors returned to clients | High |
| Executable files uploaded to public web directories | Critical |
| Missing security headers (Helmet not used) | Medium |
| HTTP without HTTPS redirect in production | High |

## Hard Bans

- No `Access-Control-Allow-Origin: *` together with credentials
- No production stack traces returned to users
- No debug mode enabled in production
- No uploading executable files into public web directories
- No missing body limits on public JSON endpoints
- No raw database or provider errors returned to clients

## Required Headers

Where applicable, configure:

| Header | Purpose |
|--------|---------|
| `Content-Security-Policy` | Restrict script/style/load sources |
| `X-Content-Type-Options: nosniff` | Prevent MIME sniffing |
| `Referrer-Policy` | Control referrer leakage |
| `Permissions-Policy` | Restrict browser features |
| `Strict-Transport-Security` | Enforce HTTPS |
| `X-Frame-Options` or CSP `frame-ancestors` | Prevent clickjacking |

## Implementation Examples

### Express with Helmet

```javascript
import helmet from 'helmet';
import cors from 'cors';

app.use(helmet());

const allowedOrigins = ['https://app.example.com', 'http://localhost:5173'];
app.use(cors({
  origin(origin, callback) {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
}));
```

### Sanitized error responses

```javascript
app.use((err, req, res, next) => {
  console.error(err); // log server-side only
  res.status(err.status || 500).json({
    error: process.env.NODE_ENV === 'production'
      ? 'Internal server error'
      : err.message,
  });
});
```

### Request limits

```javascript
app.use(express.json({ limit: '100kb' }));
```

### HTTPS enforcement

```javascript
if (process.env.NODE_ENV === 'production') {
  app.use((req, res, next) => {
    if (req.headers['x-forwarded-proto'] !== 'https') {
      return res.redirect(301, `https://${req.headers.host}${req.url}`);
    }
    next();
  });
}
```

### Dependency audit

```bash
npm audit
npm audit fix
```

Run in CI; address high/critical findings before deploy.

## File Upload Security

- Validate MIME type and size
- Generate server-side filenames
- Store outside executable web directories
- Require authentication for uploads
- Scan or restrict executable types (.exe, .sh, .php, .js if served statically)

## Verification Checklist

- [ ] CORS uses explicit allowlist
- [ ] Error responses generic to users; details logged server-side
- [ ] Security headers configured (Helmet or equivalent)
- [ ] HTTPS used in production
- [ ] Request and upload size limits exist
- [ ] Debug mode disabled in production
- [ ] Dependency audit process exists

## False-Positive Guidance

- CORS `*` without credentials on fully public read-only API — lower risk; still prefer allowlist
- Verbose errors in development — expected; gate by NODE_ENV
- Internal microservices without browser clients — CORS may not apply

## Remediation Steps

1. Replace wildcard CORS with allowlist
2. Add Helmet or equivalent headers
3. Sanitize error handler
4. Set body/upload limits
5. Enable HTTPS and HSTS
6. Run dependency audit
