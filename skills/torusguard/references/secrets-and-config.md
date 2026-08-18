# Secrets and Environment Configuration

## Scope

Prevent secrets, passwords, API keys, and privileged configuration from being committed, logged, exposed in browser bundles, or shipped through public environment variables.

## Threat Model

- Attackers scan GitHub for leaked credentials
- Browser bundles expose all client-side env vars
- Logs and error messages leak tokens
- CI configs accidentally embed production secrets

## Detection Patterns

Search for:

| Pattern | Severity |
|---------|----------|
| `.env` tracked in Git (`git ls-files .env`) | Critical |
| Hardcoded `sk_live_`, `sk_test_`, `AKIA`, `ghp_`, `gho_` | Critical |
| JWT secrets in source: `jwt.sign(..., 'hardcoded')` | Critical |
| Database URLs: `postgres://`, `mysql://`, `mongodb+srv://` in source | Critical |
| Supabase service-role key in frontend | Critical |
| Firebase Admin SDK in client code | Critical |
| `VITE_*`, `NEXT_PUBLIC_*`, `REACT_APP_*` holding secrets | High |
| Weak defaults: `admin123`, `password`, `secret`, `changeme` | High |
| Secrets in comments or test fixtures committed to repo | Medium |

## Hard Bans

- Never hardcode a database URL in source code
- Never hardcode a JWT signing secret
- Never hardcode a password in production code
- Never expose service-role or admin credentials in the browser
- Never log passwords, tokens, session identifiers, API keys, or full authorization headers
- Never treat frontend environment variables as secret

## Required Safe Defaults

1. Move secrets to server-only environment variables
2. Add `.env` to `.gitignore`
3. Provide `.env.example` with placeholder values only
4. Tell developers to **revoke and rotate** any discovered leaked secret
5. Frontend receives only public configuration (API base URL, public anon keys)

### `.env.example` template

```env
# Server-only — never prefix with VITE_, NEXT_PUBLIC_, or REACT_APP_
DATABASE_URL=postgresql://user:password@localhost:5432/myapp
JWT_SECRET=generate-a-long-random-string
STRIPE_SECRET_KEY=sk_test_xxx

# Client-safe public values only
VITE_API_URL=http://localhost:3001
VITE_SUPABASE_ANON_KEY=your-anon-key
```

### Express: load secrets server-side only

```javascript
// server/config.js
import 'dotenv/config';

const required = ['DATABASE_URL', 'JWT_SECRET'];
for (const key of required) {
  if (!process.env[key]) throw new Error(`Missing env: ${key}`);
}

export const config = {
  databaseUrl: process.env.DATABASE_URL,
  jwtSecret: process.env.JWT_SECRET,
};
```

### Next.js: server vs client env

```javascript
// Server-only — no NEXT_PUBLIC_ prefix
const dbUrl = process.env.DATABASE_URL;

// Client-safe
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

## Framework-Specific Notes

| Stack | Rule |
|-------|------|
| Vite | Only `VITE_*` vars reach client; never put secrets there |
| Next.js | `NEXT_PUBLIC_*` is bundled; everything else is server-only |
| Create React App | `REACT_APP_*` is bundled |
| Supabase | Anon key in browser OK; service-role key server-only |
| Firebase | Client config is public; Admin SDK credentials server-only |

## Verification Checklist

- [ ] No real secrets in tracked source files
- [ ] `.env` is in `.gitignore`
- [ ] `.env.example` exists with placeholders only
- [ ] No privileged secret in client-side code or public env vars
- [ ] App starts with documented environment variables

## False-Positive Guidance

- **Placeholder strings** in `.env.example` — expected, not a finding
- **Test mocks** with fake keys like `test-jwt-secret-for-ci-only` in test files — OK if clearly fake and not production values
- **Public Supabase anon key** — expected in frontend when RLS is enabled

## Remediation Steps

1. Remove secret from source immediately
2. Rotate/revoke the compromised credential
3. Move to environment variable or secret manager
4. Add pre-commit hook or CI check for secret patterns (future CLI)
