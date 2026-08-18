# TG-SEC-002: Secrets in Public Environment Variables

## Severity
Critical

## Applies To
- Frontend frameworks exposing build-time env vars to browser bundles
- Vite (`VITE_*`), Next.js (`NEXT_PUBLIC_*`), CRA (`REACT_APP_*`)
- Client-rendered pages, static exports, and edge-delivered frontend assets
- Monorepos where frontend apps consume shared environment files

## Why It Matters
Public-prefixed environment variables are intentionally embedded into shipped JavaScript and are readable by any user.  
Placing API secrets, private signing keys, or privileged service credentials in these variables effectively publishes them.  
Exposure allows unauthorized API usage, quota theft, account compromise, and backend pivoting.

## What TorusGuard Looks For
- Secret-like values assigned to `VITE_*`, `NEXT_PUBLIC_*`, or `REACT_APP_*`
- Names suggesting private intent despite public prefix:
  - `VITE_JWT_SECRET`
  - `NEXT_PUBLIC_DB_PASSWORD`
  - `REACT_APP_SERVICE_ROLE_KEY`
- Long tokens, private keys, and credential URLs in frontend env config
- Client code directly reading sensitive public variables for auth or data access
- Build scripts promoting server-only variables into public namespaces

## Unsafe Example
```env
# .env.production
NEXT_PUBLIC_STRIPE_SECRET_KEY=sk_live_51N9x...
VITE_DB_URL=postgres://admin:supersecret@db.prod:5432/core
REACT_APP_JWT_SIGNING_KEY=prod_signing_key_q2f8j1
```

```ts
// src/lib/payments.ts
export const stripeSecret = process.env.NEXT_PUBLIC_STRIPE_SECRET_KEY!;
```

## Safe Example
```env
# .env.production
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_51N9x...
```

```ts
// src/lib/payments.ts
export async function createCheckoutSession(cartId: string) {
  const res = await fetch("/api/checkout/session", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ cartId }),
  });
  return res.json();
}
```

## Remediation (numbered)
1. Remove secrets from every `VITE_*`, `NEXT_PUBLIC_*`, and `REACT_APP_*` variable.
2. Move sensitive values to server-only environment variables without public prefixes.
3. Route privileged operations through backend APIs with access control.
4. Rotate all credentials that were exposed in public frontend environments.
5. Rebuild and redeploy frontend assets after variable cleanup.
6. Add CI policy checks blocking secret-like values in public env namespaces.
7. Update team docs to separate publishable keys from secret keys explicitly.

## Verification
- Inspect built bundles to ensure no secret values are embedded.
- Validate frontend only references publishable or non-sensitive config.
- Confirm backend endpoints own all privileged API calls.
- Check environment templates for corrected naming and scope boundaries.
- Ensure old exposed keys fail when tested after rotation.

## False Positives and Exceptions
- Publishable keys (for example, Stripe publishable key) are acceptable by design.
- Public feature flags and app metadata can safely use public prefixes.
- A value that looks random is not always secret; validate provider classification.
- Exceptions require documented approval and periodic re-review.

## Related Rules
- [TG-SEC-001](./TG-SEC-001-hardcoded-secrets.md) - Hardcoded credential literals in source code
- [TG-DB-002](./TG-DB-002-privileged-database-credential.md) - Privileged DB credentials exposed in browser code
- [TG-DB-003](./TG-DB-003-frontend-admin-sdk.md) - Frontend use of admin/server-only SDKs
