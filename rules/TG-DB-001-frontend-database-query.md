# TG-DB-001: Frontend Database Query Logic

## Severity
High

## Applies To
- Frontend source paths such as `src/`, `app/`, `pages/`, `components/`, `client/`, `public/`
- Browser-executed JavaScript and TypeScript bundles
- SSR-hybrid projects where code placement can blur server/client boundaries
- Shared utility modules imported by frontend entry points

## Why It Matters
Executing SQL construction or raw database access logic in frontend code exposes internal schema assumptions and trust boundaries.  
Even if direct DB connectivity fails in browsers, query logic can leak sensitive structure, encourage insecure architecture, and lead to credential exposure attempts.  
Database interaction must stay on trusted server infrastructure with controlled authorization.

## What TorusGuard Looks For
- SQL strings (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) in frontend-scoped files
- Query builders or DB clients imported into client-rendered modules
- Functions assembling SQL fragments from user input in browser code
- Mentions of table names, admin joins, or migration SQL in UI components
- Direct network calls from frontend intended for database endpoints

## Unsafe Example
```ts
// src/components/UserLookup.tsx
export function loadUserByEmail(email: string) {
  const sql = `SELECT id, role FROM users WHERE email = '${email}' LIMIT 1`;

  return fetch("/db/query", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ sql }),
  }).then((r) => r.json());
}
```

## Safe Example
```ts
// src/components/UserLookup.tsx
export function loadUserByEmail(email: string) {
  return fetch("/api/users/lookup", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ email }),
  }).then((r) => r.json());
}
```

```ts
// server/routes/users.ts
app.post("/api/users/lookup", async (req, res) => {
  const user = await userRepo.findByEmail(req.body.email);
  res.json({ id: user?.id, role: user?.role ?? "none" });
});
```

## Remediation (numbered)
1. Remove SQL strings and database query logic from frontend-scoped files.
2. Move all data access into backend APIs, repositories, or service layers.
3. Validate and authorize request parameters on the server before querying.
4. Return minimal response shapes needed by the UI.
5. Review frontend imports to prevent accidental DB client inclusion.
6. Add static checks that disallow SQL keywords in client-targeted directories.
7. Document architecture boundaries between browser code and data layers.

## Verification
- Scan frontend paths for SQL keywords and DB client imports.
- Confirm browser bundles contain no query builders or SQL literals.
- Validate data retrieval flows through authenticated backend endpoints.
- Test unauthorized requests to ensure server-side access controls hold.
- Review code ownership and lint rules enforcing client/server separation.

## False Positives and Exceptions
- Static tutorial snippets in markdown may contain SQL and are non-executable.
- Demo strings in tests are acceptable if isolated from production bundles.
- Client files that only reference SQL terms in copy text are low risk.
- Exceptions should be time-bound and approved by architecture owners.

## Related Rules
- [TG-DB-002](./TG-DB-002-privileged-database-credential.md) - Privileged DB credentials in browser exposure
- [TG-DB-003](./TG-DB-003-frontend-admin-sdk.md) - Admin/server SDK usage in frontend code
- [TG-SEC-002](./TG-SEC-002-public-environment-secrets.md) - Public-prefixed secret leakage
