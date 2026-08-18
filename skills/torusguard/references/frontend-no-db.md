# Frontend Database Protection

## Scope

Ensure the browser never directly contains raw database queries, privileged database clients, database connection strings, or admin SDK credentials.

## Threat Model

- Attackers read all JavaScript delivered to the browser
- Direct DB access from frontend bypasses authorization
- Service-role keys grant full database access
- Client-side "hidden admin routes" are not access control

## Core Rule

The frontend may call an authenticated API. The backend or trusted server function performs authorization and database operations.

## Frontend Directories to Scan

```
src/
app/
pages/
components/
client/
public/
```

## Detection Patterns

| Pattern | Severity |
|---------|----------|
| SQL keywords in frontend: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER` | Critical |
| Imports: `pg`, `mysql`, `mysql2`, `mongoose`, `@prisma/client`, `sequelize`, `typeorm` | Critical |
| Connection strings: `postgres://`, `mysql://`, `mongodb+srv://` | Critical |
| `firebase-admin`, Supabase service-role key usage | Critical |
| Prisma client in React/Vue components | Critical |
| `createClient(url, serviceRoleKey)` in frontend | Critical |

## Hard Bans

- No SQL query may exist in frontend files
- No database driver may be imported by frontend files
- No service-role key, admin key, or database connection string may ship to the browser
- No client-provided user ID or role may be trusted without server-side verification
- No client-side "hidden admin route" may be considered access control

## Safe Architecture

```
React/Vite/Next client
        |
        | HTTPS request with validated payload
        v
Express route / Next server action / Edge function
        |
        | authenticate user + authorize action
        v
Parameterized database query / ORM
        |
        v
Database
```

### Unsafe (never allow)

```javascript
// frontend file — NEVER
const result = await db.query(
  `SELECT * FROM users WHERE email = '${email}'`
);
```

### Safe pattern

```javascript
// frontend — call API only
const res = await fetch('/api/users/me', { credentials: 'include' });
const user = await res.json();
```

```javascript
// server/routes/users.js
router.get('/me', requireAuth, async (req, res) => {
  const user = await db.query('SELECT id, email FROM users WHERE id = $1', [req.user.id]);
  res.json(user.rows[0]);
});
```

## Supabase Requirements

- Browser clients use **anon/public key only**
- Row Level Security (RLS) **enabled** on all exposed tables
- Service-role key **server-only**
- Policies verify ownership and role requirements

```sql
-- Example RLS policy
CREATE POLICY "Users read own profile"
  ON profiles FOR SELECT
  USING (auth.uid() = user_id);
```

## Firebase Requirements

- Client SDK constrained by **Firebase Security Rules**
- Admin SDK **server-only**
- Rules verify ownership and role requirements

```javascript
// firestore.rules — verify ownership
match /users/{userId} {
  allow read, write: if request.auth != null && request.auth.uid == userId;
}
```

## Verification Checklist

- [ ] No frontend directory contains DB credentials or driver imports
- [ ] All database operations go through trusted server path or secure BaaS policies
- [ ] Each data mutation verifies authenticated user's authorization
- [ ] Supabase RLS enabled (manual review)
- [ ] Firebase rules deployed (manual review)

## False-Positive Guidance

- SQL strings in **server** directories (`server/`, `api/`, `app/api/`) — expected
- ORM query builders in Next.js **server components** or **route handlers** — OK
- Display text containing "SELECT" in UI copy — not a finding

## Remediation Steps

1. Remove DB client/query from frontend file
2. Create API endpoint or server action
3. Add authentication and authorization on server
4. Use parameterized queries on server side
