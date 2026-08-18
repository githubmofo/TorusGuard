# Frontend Database Protection

## When to load

Load during `/torusguard check database`, full-stack audits, or when frontend code connects to data stores.

## Linked rules

- [TG-DB-001](../../rules/TG-DB-001-frontend-database-query.md) — Database Query in Frontend (High)
- [TG-DB-002](../../rules/TG-DB-002-privileged-database-credential.md) — Privileged Credential in Browser (Critical)
- [TG-DB-003](../../rules/TG-DB-003-frontend-admin-sdk.md) — Frontend Admin SDK (Critical)

## Hard bans

- No SQL in frontend directories (`src/`, `app/`, `pages/`, `components/`, `client/`, `public/`)
- No imports of `pg`, `mysql`, `mongoose`, `@prisma/client`, Sequelize, TypeORM, Drizzle server client
- No Supabase service-role key or Firebase Admin SDK in browser code
- No trust in client-provided user ID or role without server verification

## Safe architecture

```
Browser → HTTPS API → AuthZ → Parameterized query/ORM → Database
```

## Supabase

- Browser: anon key + **RLS enabled** on all exposed tables
- Server: service-role key only for admin tasks
- **Manual review required:** RLS policies for every table

## Firebase

- Browser: client SDK + Security Rules
- Server: Admin SDK only
- **Manual review required:** Firestore/Storage rules

## Audit checklist

- [ ] No DB queries or drivers in client code (TG-DB-001, TG-DB-003)
- [ ] No connection strings or service-role keys in bundle (TG-DB-002)
- [ ] All mutations authorized server-side
- [ ] Supabase RLS / Firebase rules reviewed and tested

## Framework guides

- [Supabase](../../guides/supabase-security.md)
- [Firebase](../../guides/firebase-security.md)
- [React/Vite](../../guides/react-vite-security.md)

## Related rules

TG-SEC-002, TG-AUTH-002, TG-AUTH-003
