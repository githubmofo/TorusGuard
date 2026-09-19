# Next.js Security Guide

## When to use

Load during audits of Next.js App Router or Pages Router applications.

**Related rules:** TG-SEC-002, TG-DB-003, TG-AUTH-002, TG-AUTH-003, TG-CLIENT-001, TG-PLATFORM-002

## Server vs client boundary

| Location | Can use secrets? | Can access DB? |
|----------|------------------|----------------|
| Server Components, Route Handlers, Server Actions | Yes (env without `NEXT_PUBLIC_`) | Yes (server SDK) |
| Client Components (`'use client'`) | No | No |

Never import server-only modules (Prisma, `pg`, Firebase Admin, service-role Supabase) into Client Components.

## Checklist

- [ ] No `NEXT_PUBLIC_*` variables hold secrets (TG-SEC-002)
- [ ] Route handlers and Server Actions validate input and authorize users
- [ ] `productionBrowserSourceMaps: false` in production
- [ ] Cookie sessions use httpOnly, Secure, SameSite (TG-AUTH-004)
- [ ] CSRF considered for cookie-authenticated mutations
- [ ] Sensitive data not over-cached in public CDN routes
- [ ] Security headers via `next.config` or middleware/Helmet on custom server

## Environment variables

```env
# Server-only
DATABASE_URL=postgresql://...
JWT_SECRET=...

# Client-safe
NEXT_PUBLIC_API_URL=https://api.example.com
```

## Route handler pattern

```typescript
// app/api/orders/[id]/route.ts
import { z } from 'zod';
import { getSession } from '@/lib/session';
import { db } from '@/lib/db';

const paramsSchema = z.object({ id: z.string().uuid() });

export async function GET(req: Request, { params }: { params: { id: string } }) {
  const session = await getSession();
  if (!session) return Response.json({ error: 'Unauthorized' }, { status: 401 });

  const parsed = paramsSchema.safeParse(params);
  if (!parsed.success) return Response.json({ error: 'Invalid input' }, { status: 400 });

  const order = await db.order.findFirst({
    where: { id: parsed.data.id, userId: session.userId },
  });
  if (!order) return Response.json({ error: 'Not found' }, { status: 404 });

  return Response.json(order);
}
```

## Server Actions

Validate and authorize at the start of every Server Action. Do not trust hidden form fields for `role` or `userId`.

## Source maps

```javascript
// next.config.js
const nextConfig = {
  productionBrowserSourceMaps: false,
};
export default nextConfig;
```

## CSRF and sessions

When using cookie-based auth with Server Actions or form POSTs, verify Origin/Referer or use CSRF tokens for state-changing requests.

## Cache and privacy

Avoid caching personalized responses at CDN edge unless intentionally public. Review `fetch` cache options and `revalidate` settings for user-specific data.

## Manual review

- Trace every `'use client'` file for accidental secret imports
- Test IDOR on dynamic `[id]` routes (TG-AUTH-003)
- Review middleware auth coverage

## Related documentation

- [rules/TG-AUTH-003-missing-object-authorization.md](../rules/TG-AUTH-003-missing-object-authorization.md)
- [guides/express-security.md](express-security.md) (custom server)
