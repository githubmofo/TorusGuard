# TG-DB-002: Privileged Database Credential in Browser Context

## Severity
Critical

## Applies To
- Browser-executed code in frontend apps and static assets
- Public environment variables consumed by client bundles
- Mobile web, desktop web, and embedded webview clients
- Shared modules imported into client-side runtime

## Why It Matters
Privileged database credentials in browser-accessible code grant attackers direct or indirect control over sensitive data stores.  
Service-role keys and admin database URLs typically bypass row-level access controls and can expose full datasets.  
Because frontend artifacts are publicly retrievable, embedded privileged credentials should be treated as compromised.

## What TorusGuard Looks For
- Service-role keys and admin tokens referenced in frontend code
- Database URLs containing usernames/passwords in browser-executed modules
- Public env variables with names such as:
  - `NEXT_PUBLIC_DATABASE_URL`
  - `VITE_SUPABASE_SERVICE_ROLE_KEY`
  - `REACT_APP_ADMIN_DB_TOKEN`
- Client initialization using elevated credentials intended for server trust zones
- Fallback credential constants used when env vars are missing

## Unsafe Example
```ts
// src/lib/dbClient.ts
import { createClient } from "@supabase/supabase-js";

const url = process.env.NEXT_PUBLIC_DATABASE_URL!;
const serviceRole = process.env.NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY!;

export const db = createClient(url, serviceRole, {
  auth: { persistSession: false },
});
```

## Safe Example
```ts
// src/lib/publicClient.ts
import { createClient } from "@supabase/supabase-js";

const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export const publicDb = createClient(url, anonKey);
```

```ts
// server/lib/adminDb.ts
import { createClient } from "@supabase/supabase-js";

export const adminDb = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!,
);
```

## Remediation (numbered)
1. Remove privileged DB credentials from all frontend and public env sources.
2. Rotate exposed service-role keys, passwords, and privileged tokens immediately.
3. Migrate privileged operations to backend-only services and APIs.
4. Use least-privilege client credentials (anonymous/public keys) in browser code.
5. Audit access logs for misuse during exposure window.
6. Enforce CI policy blocking privileged credential names in public scopes.
7. Add architecture documentation defining credential trust boundaries.

## Verification
- Inspect client bundles and source maps for privileged credential artifacts.
- Confirm frontend uses only non-privileged credentials and constrained APIs.
- Validate server-only secrets are loaded from private runtime environments.
- Test rotated privileged credentials and verify old keys are rejected.
- Review monitoring for anomalous database access during and after remediation.

## False Positives and Exceptions
- Public anonymous keys may look secret-like but are intentionally non-privileged.
- Documentation examples can trigger detections; verify they are non-operational.
- Local-only sandbox credentials are still risky if bundled into distributed builds.
- Exceptions require security approval, owner assignment, and expiration date.

## Related Rules
- [TG-SEC-001](./TG-SEC-001-hardcoded-secrets.md) - Hardcoded secrets in tracked source
- [TG-SEC-002](./TG-SEC-002-public-environment-secrets.md) - Secrets in public env namespaces
- [TG-DB-003](./TG-DB-003-frontend-admin-sdk.md) - Admin SDK usage in frontend runtime
