# TG-DB-003: Frontend Use of Admin or Server-Only Database SDKs

## Severity
Critical

## Applies To
- Frontend directories such as `src/`, `app/`, `pages/`, `components/`, `client/`, `public/`
- Browser bundles in React, Next.js client components, Vite, and CRA
- Shared package imports consumed by client entry points
- Build systems that can accidentally include server-only dependencies

## Why It Matters
Admin SDKs and server drivers are designed for trusted environments and often assume unrestricted credentials and network access.  
Using packages like Firebase Admin, Prisma, or `pg` in frontend paths risks exposing privileged behavior, credentials, and internal data models.  
Even failed browser execution can leak sensitive implementation details and weaken architectural boundaries.

## What TorusGuard Looks For
- Imports of server-only SDKs in frontend-targeted files:
  - `firebase-admin`
  - `@prisma/client`
  - `pg`
- Initialization logic for admin clients in UI components or client utilities
- Conditional imports attempting to bypass bundler checks in browser code
- Code patterns that create server DB connections in frontend modules
- Shared files that instantiate privileged clients and are imported by frontend

## Unsafe Example
```ts
// src/app/dashboard/adminMetrics.tsx
import { PrismaClient } from "@prisma/client";
import { Client } from "pg";

const prisma = new PrismaClient();
const pgClient = new Client({
  connectionString: process.env.NEXT_PUBLIC_DATABASE_URL,
});

export async function loadMetrics() {
  await pgClient.connect();
  const result = await prisma.user.count();
  return { users: result };
}
```

## Safe Example
```ts
// src/app/dashboard/adminMetrics.tsx
export async function loadMetrics() {
  const res = await fetch("/api/admin/metrics", { method: "GET" });
  return res.json();
}
```

```ts
// server/routes/adminMetrics.ts
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

app.get("/api/admin/metrics", async (_req, res) => {
  const users = await prisma.user.count();
  res.json({ users });
});
```

## Remediation (numbered)
1. Remove server-only SDK imports from frontend and browser-targeted modules.
2. Relocate privileged data access to backend routes, jobs, or server actions.
3. Ensure frontend calls authenticated backend endpoints for required data.
4. Restrict server-only dependencies to backend package boundaries.
5. Configure bundler/lint rules to block admin SDK imports in frontend paths.
6. Rotate credentials if admin SDK usage exposed privileged config values.
7. Add architecture tests validating strict client/server dependency separation.

## Verification
- Scan frontend directories for imports of `firebase-admin`, Prisma, and `pg`.
- Confirm build output excludes server-only database packages in client chunks.
- Validate admin operations execute only on server infrastructure.
- Run access-control tests against backend endpoints exposing admin data.
- Review dependency graphs to ensure no frontend transitive path to admin SDKs.

## False Positives and Exceptions
- Type-only imports can appear suspicious; verify they are erased at build time.
- Documentation snippets in markdown are non-runtime and may be acceptable.
- Server components must be verified carefully to avoid accidental client inclusion.
- Exceptions require documented risk acceptance and periodic security review.

## Related Rules
- [TG-DB-001](./TG-DB-001-frontend-database-query.md) - Frontend SQL/query logic anti-pattern
- [TG-DB-002](./TG-DB-002-privileged-database-credential.md) - Privileged credential exposure in browser
- [TG-SEC-001](./TG-SEC-001-hardcoded-secrets.md) - Hardcoded sensitive literals in source
