# TG-GQL-001: Missing Query Depth or Complexity Limits

## Severity
High. Unbounded GraphQL queries allow nested recursive queries (e.g., author $\rightarrow$ books $\rightarrow$ author) that trigger server denial-of-service, CPU saturation, and exponential database query loads.

## Applies To
- Apollo Server, Yoga, GraphQL.js, Strawberry, Graphene (Python), TypeGraphQL

## Why It Matters
GraphQL allows client-controlled response structures. Without depth limiting or cost analysis:
1. An attacker can submit deeply nested circular queries ($> 100$ levels) that monopolize Node.js or Python event loops.
2. Batching multiple expensive queries in a single HTTP request bypasses naive rate limiters.
3. Automated scanners can trigger denial-of-service unless runtime introspection probes are bounded to harmless depth thresholds.

## What TorusGuard Looks For
1. GraphQL server setup lacking query depth validation rules (e.g., `graphql-depth-limit`).
2. Missing complexity/cost calculation plugins (`graphql-query-complexity`).
3. Runtime probe: Executing a harmless 3-level bounded query canary; flagging if queries deeper than allowed thresholds execute without validation errors.

## Unsafe Example
```typescript
// UNSAFE: Apollo Server without query depth or complexity validation
import { ApolloServer } from "@apollo/server";

const server = new ApolloServer({
  typeDefs,
  resolvers,
  // No depth limit or complexity plugins configured!
});
```

## Safe Example
```typescript
// SAFE: Query depth validation capped at 6 levels and complexity cost limits
import { ApolloServer } from "@apollo/server";
import depthLimit from "graphql-depth-limit";
import { createComplexityLimitRule } from "graphql-validation-complexity";

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    depthLimit(6), // Maximum query nesting depth
    createComplexityLimitRule(1000, {
      onCost: (cost) => console.log(`GraphQL Query Cost: ${cost}`),
    }),
  ],
});
```

## Bounded Runtime Probe Protocol
When probing GraphQL endpoints under `/torusguard web-validate`:
1. Submit a **bounded 3-level canary query** (e.g., `{ __typename, schema: __schema { types { name } } }`).
2. Submit a single test query exceeding max depth (e.g., 7 levels) with a strict request budget of 1 request.
3. Assert that the server responds with an HTTP 400 or GraphQL `GRAPHQL_VALIDATION_FAILED` error rather than evaluating resolvers.

## Remediation
1. **Enforce Depth Limiting:** Install `graphql-depth-limit` and cap maximum depth (typically 5–7 levels).
2. **Implement Query Cost Analysis:** Assign complexity points per field and reject queries exceeding cost thresholds.
3. **Disable Production Introspection:** Set `introspection: false` in production environments.

## Related Rules
- `TG-GQL-004`: Unnecessary Production Introspection
- `TG-RATE-003`: Unbounded Resource Consumption
