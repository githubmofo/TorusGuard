# TG-GQL-002: GraphQL Resolver Missing Authorization

## Severity
High. Exposing GraphQL mutation or query resolvers without granular user ownership or role authorization checks allows authenticated users to query or mutate records belonging to other tenants.

## Applies To
- GraphQL Servers (Apollo Server, Yoga, Pothos, Graphene)
- Node.js, Python, Go, Java

## Why It Matters
In GraphQL, nested queries allow clients to traverse relationships (e.g. `user { organization { members { invoices } } }`). If individual field resolvers fail to assert ownership, users can traverse schema graphs to access unauthorized tenant resources.

## What TorusGuard Looks For
- GraphQL resolver functions querying database entities directly by `args.id` without checking `context.user` or filtering by `context.tenantId`.

## Unsafe Example
```javascript
// UNSAFE: Querying invoice directly by ID without checking user or tenant
const resolvers = {
  Query: {
    invoice: async (_, { id }) => {
      return await db.invoice.findUnique({ where: { id } });
    }
  }
};
```

## Safe Example
```javascript
// SAFE: Scoping query by tenant and authenticated user context
const resolvers = {
  Query: {
    invoice: async (_, { id }, context) => {
      if (!context.user) throw new Error('Unauthorized');
      return await db.invoice.findFirst({
        where: { id, tenantId: context.user.tenantId }
      });
    }
  }
};
```

## Ponytail Remediation Budget
- Additions: <= 8 lines
- Deletions: <= 2 lines

## Remediation
1. Enforce shield/guard middleware or resolver-level ownership checks on all query and mutation fields.
2. Pass authenticated `context` to all database queries and enforce `tenantId` constraints.

## Related Rules
- `TG-DB-004`: Missing Multi-Tenant Query Isolation
- `TG-AUTH-003`: Missing Object-Level Authorization (IDOR)
