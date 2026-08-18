# React + Vite Security Guide

## When to use

Load during audits of React + Vite frontends with a separate or proxied API backend.

**Related rules:** TG-SEC-002, TG-DB-001, TG-DB-002, TG-AUTH-002, TG-CLIENT-001, TG-CLIENT-002, TG-INPUT-003

## Core truth: the browser bundle is public

If the browser receives JavaScript, users can read it in DevTools, Sources, and network tabs. TorusGuard cannot block Inspect Element. Never put secrets, database credentials, or authorization decisions only in client code.

## Checklist

- [ ] No secrets in `VITE_*` environment variables
- [ ] No SQL, ORM, or DB driver imports in `src/`
- [ ] Private data fetched only through authenticated API calls
- [ ] `build.sourcemap: false` for production (TG-CLIENT-001)
- [ ] No `console.log` of tokens, users, or config in production paths
- [ ] Route guards are UX only — server enforces authorization (TG-AUTH-002)
- [ ] User HTML rendered as text unless sanitized (TG-INPUT-003)
- [ ] CSP configured at hosting/API layer where applicable

## Environment variables

Only intentionally public values belong in Vite client env:

```env
# .env.example — safe for client
VITE_API_URL=http://localhost:3001
VITE_APP_NAME=MyApp

# NEVER prefix secrets with VITE_
# JWT_SECRET, DATABASE_URL, STRIPE_SECRET_KEY → server only
```

```javascript
// vite.config.js — disable public production source maps
export default defineConfig({
  build: { sourcemap: false },
  server: {
    proxy: { '/api': 'http://localhost:3001' },
  },
});
```

## Data access pattern

```javascript
// client/src/api/users.js — safe
export async function fetchMyProfile() {
  const res = await fetch('/api/users/me', { credentials: 'include' });
  if (!res.ok) throw new Error('Unauthorized');
  return res.json();
}
```

Never construct SQL or import `pg`, `@prisma/client`, or Supabase service-role client in `src/`.

## Client route guards

```jsx
// UX redirect only — NOT security
function AdminRoute({ children }) {
  const { user } = useAuth();
  if (!user?.role) return <Navigate to="/login" />;
  return children;
}
```

Every admin action must still fail on the server without proper role checks.

## Safe rendering

```jsx
// Safe — React escapes text by default
<p>{user.bio}</p>

// High risk — only with trusted/sanitized HTML
<div dangerouslySetInnerHTML={{ __html: sanitizedHtml }} />
```

## CSP considerations

Define CSP at the reverse proxy or Express/Next layer. Account for Vite dev server in development; tighten for production with explicit `script-src`, `connect-src`, and `img-src` origins.

## Manual review

- Verify API endpoints enforce auth for every sensitive client call
- Confirm no secret accidentally added to `import.meta.env` usage
- Review third-party scripts loaded in `index.html`

## Related documentation

- [rules/TG-SEC-002-public-environment-secrets.md](../rules/TG-SEC-002-public-environment-secrets.md)
- [rules/TG-CLIENT-001-public-production-source-maps.md](../rules/TG-CLIENT-001-public-production-source-maps.md)
- [skills/torusguard/references/client-code-exposure.md](../skills/torusguard/references/client-code-exposure.md)
