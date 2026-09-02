# TG-EDGE-001: Serverless & Edge Global State Memory Leakage

## Severity
High. Global state persistence across warm container or edge worker invocations can lead to cross-request tenant pollution and unauthorized credential disclosure.

## Applies To
- Cloudflare Workers
- Vercel Edge Functions (Next.js Edge Runtime)
- AWS Lambda / Netlify Functions

## Why It Matters
In serverless and edge computing architectures:
1. **Container / Isolate Reuse:** Serverless instances (V8 isolates or MicroVMs) stay warm across sequential invocations to optimize startup latency.
2. **State Leakage Hazard:** Global variables, module-scoped arrays, singletons, or uncleaned caches persist between subsequent client requests handled by the same warm worker.
3. **Cross-Tenant Contamination:** If User A's authentication token, tenant ID, or profile data is assigned to a module-level variable, a subsequent request from User B can accidentally read User A's data without authenticating.

## What TorusGuard Looks For
1. Module-scoped or global mutable variables (`let`, `var`, global `Map`, `dict`) storing user-specific context, request headers, or auth tokens.
2. Singleton database connection pools or client sessions retaining user-specific session state across handler calls.
3. Lack of explicit request-scoped context initialization.

## Unsafe Example
```typescript
// UNSAFE: Module-scoped state persists across warm Cloudflare Worker invocations
let currentSessionUser: { id: string; role: string } | null = null;

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const token = request.headers.get("Authorization");
    if (token) {
      // Leaks to subsequent requests if not explicitly cleared on every path!
      currentSessionUser = await verifyUser(token);
    }
    
    // Danger: If next request lacks Authorization header, currentSessionUser remains set!
    return new Response(JSON.stringify({ user: currentSessionUser }));
  }
};
```

## Safe Example
```typescript
// SAFE: Strictly request-scoped context; zero mutable global state
interface RequestContext {
  user: { id: string; role: string } | null;
  requestId: string;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    // Context is created fresh per invocation inside the handler scope
    const reqContext: RequestContext = {
      user: null,
      requestId: crypto.randomUUID(),
    };

    const token = request.headers.get("Authorization");
    if (token) {
      reqContext.user = await verifyUser(token, env.JWT_SECRET);
    }

    if (!reqContext.user) {
      return new Response(JSON.stringify({ error: "Unauthorized" }), { status: 401 });
    }

    return new Response(JSON.stringify({ user: reqContext.user }));
  }
};
```

## Remediation
1. **Enforce Request-Scoped State:** Always declare mutable variables, session holders, and tenant identifiers inside the handler function scope.
2. **Treat Global Scope as Immutable:** Limit module-level variables strictly to immutable configuration constants, static schemas, or stateless utility functions.
3. **Isolate Database Clients:** Ensure database connections or ORM instances created globally do not cache user-specific transaction boundaries or credentials.

## Verification
- Unit test sequential simulated requests against the worker ensuring User A's context never appears in an unauthenticated User B invocation.
- Assert that static linters flag module-scoped mutable assignments in edge handler files.

## Related Rules
- `TG-EDGE-003`: AWS Lambda Ephemeral Execution & Cold Start Security
- `TG-AUTH-002`: Client-Side Only Authorization
- `TG-DB-004`: Missing Tenant Query Isolation
