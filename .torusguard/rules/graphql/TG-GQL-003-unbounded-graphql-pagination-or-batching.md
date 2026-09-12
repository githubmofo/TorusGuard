# TG-GQL-003: Unbounded GraphQL Pagination or Batching

## Severity
Medium. Permitting unbounded `first`, `limit`, or batching queries in GraphQL enables resource exhaustion and Denial of Service (DoS).

## Applies To
- Apollo Server, GraphQL Yoga, Graphene
- Node.js, Python, Go

## Why It Matters
Clients can request `users(first: 1000000)` or send a batched array of 500 queries in a single HTTP request, forcing the server to exhaust memory and database connection pools.

## What TorusGuard Looks For
- Resolvers accepting integer `first` / `limit` arguments without enforcing a maximum cap (e.g. `Math.min(limit, 100)`).

## Unsafe Example
```javascript
// UNSAFE: Directly passing client-controlled limit to database
const resolvers = {
  Query: {
    users: async (_, { limit = 50 }) => {
      return await db.user.findMany({ take: limit }); // Attacker passes limit: 500000
    }
  }
};
```

## Safe Example
```javascript
// SAFE: Enforcing strict maximum upper bound on pagination
const MAX_LIMIT = 100;
const resolvers = {
  Query: {
    users: async (_, { limit = 20 }) => {
      const safeLimit = Math.min(Math.max(1, limit), MAX_LIMIT);
      return await db.user.findMany({ take: safeLimit });
    }
  }
};
```

## Ponytail Remediation Budget
- Additions: <= 5 lines
- Deletions: <= 2 lines

## Remediation
1. Enforce maximum limit boundaries on all pagination arguments.
2. Disable batched HTTP query execution unless explicitly required.

## Related Rules
- `TG-RATE-003`: Unbounded Resource Consumption
- `TG-GQL-001`: Missing Query Depth Limits
