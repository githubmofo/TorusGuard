# Secure Defaults Reference

Quick-reference for secure defaults by stack. Used by TorusGuard reference modules.

## Environment Variables

| Variable type | Prefix | Reaches browser? |
|---------------|--------|------------------|
| Vite client | `VITE_` | Yes |
| Next.js public | `NEXT_PUBLIC_` | Yes |
| CRA public | `REACT_APP_` | Yes |
| Server-only | (none) | No |

**Rule:** Only public, non-secret values get client prefixes.

## Password Hashing

| Algorithm | Status |
|-----------|--------|
| Argon2id | Preferred |
| bcrypt (cost ≥ 12) | Acceptable |
| scrypt | Acceptable |
| SHA256 alone | Reject |
| MD5 / SHA1 | Reject |
| Plaintext | Reject |

## Cookie Flags (production)

```
httpOnly: true
secure: true
sameSite: 'lax' | 'strict'
```

## Rate Limit Starting Points

| Endpoint | Default |
|----------|---------|
| Login | 5 / IP / 15 min |
| Password reset | 3 / email / hour |
| OTP send | 3 / identifier / 15 min |
| Contact form | 5 / IP / hour |
| Public API | 60 / IP / minute |

## Source Maps

| Framework | Production setting |
|-----------|-------------------|
| Vite | `build.sourcemap: false` |
| Next.js | `productionBrowserSourceMaps: false` |
| CRA | `GENERATE_SOURCEMAP=false` |

## CORS

```javascript
// Safe: explicit allowlist
origin: ['https://app.example.com']

// Unsafe: wildcard + credentials
origin: '*', credentials: true  // NEVER
```

## SQL

```javascript
// Safe
db.query('SELECT * FROM users WHERE id = $1', [id]);

// Unsafe
db.query(`SELECT * FROM users WHERE id = '${id}'`);
```

## Supabase

- Browser: anon key + RLS enabled
- Server: service-role key only
- Every table exposed to client must have RLS policies

## Firebase

- Browser: client SDK + security rules
- Server: Admin SDK only
- Rules must verify `request.auth.uid` for user data

## Error Responses

```javascript
// Production
res.status(500).json({ error: 'Internal server error' });

// Development only
res.status(500).json({ error: err.message });
```

## Request Limits

```javascript
express.json({ limit: '100kb' })
// Upload: validate MIME, size, auth; store outside web root
```

## Security Headers (via Helmet)

- Content-Security-Policy
- X-Content-Type-Options: nosniff
- Strict-Transport-Security
- X-Frame-Options / frame-ancestors
- Referrer-Policy
- Permissions-Policy
