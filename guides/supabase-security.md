# Supabase Security Guide

## When to use

Load during audits of applications using Supabase Auth, Database, or Storage.

**Related rules:** TG-DB-002, TG-DB-003, TG-AUTH-003, TG-SEC-002

## Key distinction

| Key | Where | Purpose |
|-----|-------|---------|
| **anon (public) key** | Browser OK | Client SDK with RLS enforced |
| **service-role key** | Server only | Bypasses RLS — never in frontend |

Violating this mapping triggers TG-DB-002 (Critical) and TG-DB-003 (Critical).

## Checklist

- [ ] Service-role key only in server/edge functions
- [ ] RLS enabled on every table exposed to client
- [ ] Policies verify `auth.uid()` ownership or role
- [ ] Storage bucket policies restrict read/write by user
- [ ] No sensitive logic relying only on client-side filters
- [ ] Server-only admin actions use service-role in trusted environment

## Browser client (safe)

```javascript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_ANON_KEY
);
```

## Server admin (safe)

```javascript
// server/admin.js — never import in client bundle
import { createClient } from '@supabase/supabase-js';

const admin = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);
```

## RLS policy example

```sql
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users read own profile"
  ON profiles FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = user_id);
```

## Manual RLS review checklist

For each table reachable from the browser:

1. Is RLS enabled?
2. Does SELECT policy prevent cross-user reads?
3. Do INSERT/UPDATE/DELETE policies verify ownership?
4. Are admin-only tables blocked for anon/authenticated roles?
5. Test with two user sessions — User A must not read User B rows

Document review date in project `SECURITY.md`.

## Storage

Apply bucket policies mirroring database ownership. Do not use public buckets for private user files without signed URL strategy.

## Related documentation

- [rules/TG-DB-002-privileged-database-credential.md](../rules/TG-DB-002-privileged-database-credential.md)
- [rules/TG-DB-003-frontend-admin-sdk.md](../rules/TG-DB-003-frontend-admin-sdk.md)
- [skills/torusguard/references/frontend-no-db.md](../skills/torusguard/references/frontend-no-db.md)
