# TG-GQL-004: Unnecessary Production Introspection

## Severity
Medium. Enabling GraphQL schema introspection in production environments reveals full schema types, queries, mutations, and deprecated fields to external attackers.

## Applies To
- GraphQL Servers (Apollo, Yoga, Mercurius, Helix)
- Production Node.js, Python, Go deployments

## Why It Matters
While introspection powers developer tools like Apollo Studio and GraphiQL, in production it provides attackers with an automated blueprint of the internal API surface, administrative fields, and hidden parameters.

## What TorusGuard Looks For
- GraphQL server initialization setting `introspection: true` or failing to disable introspection when `NODE_ENV === 'production'`.

## Unsafe Example
```javascript
// UNSAFE: Introspection unconditionally enabled
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: true
});
```

## Safe Example
```javascript
// SAFE: Introspection restricted to non-production environments
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== 'production'
});
```

## Ponytail Remediation Budget
- Additions: <= 2 lines
- Deletions: <= 2 lines

## Remediation
1. Bind `introspection` to environment checks (`process.env.NODE_ENV !== 'production'`).
2. Disable GraphQL Playground and Apollo Sandbox in production.

## Related Rules
- `TG-PLATFORM-003`: Production Stack Trace Exposure
- `TG-CLIENT-001`: Public Production Source Maps
