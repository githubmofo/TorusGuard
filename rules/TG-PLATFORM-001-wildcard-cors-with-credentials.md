# TG-PLATFORM-001: Wildcard CORS With Credentials

## Severity

High

## Applies To

- API servers configuring CORS headers
- Express/Fastify/Nest middleware using `cors()` defaults
- Reverse proxies and gateways injecting `Access-Control-*` headers
- Session or cookie-authenticated APIs consumed by browsers
- Multi-tenant APIs with dynamic origin reflection logic

## Why It Matters

Credentialed cross-origin requests require strict origin controls.
Using wildcard origins with credentials breaks browser security guarantees.
Misconfigurations can expose authenticated responses to untrusted origins.
Even partial origin reflection bugs can create cross-site data leakage.
This often appears as a simple config mistake with severe impact.

## What TorusGuard Looks For

- `Access-Control-Allow-Origin: *` combined with `Access-Control-Allow-Credentials: true`
- CORS middleware configured with `origin: true` without allowlist validation
- Reflecting any incoming `Origin` header directly back in responses
- Missing per-environment allowlists for trusted frontends
- Inconsistent preflight handling between gateway and application
- Session-cookie APIs that allow broad or dynamic untrusted origins

## Unsafe Example

```ts
import cors from "cors";

app.use(cors({
  origin: "*",
  credentials: true
}));
```

```ts
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", req.headers.origin || "*");
  res.setHeader("Access-Control-Allow-Credentials", "true");
  next();
});
```

## Safe Example

```ts
import cors from "cors";

const allowedOrigins = new Set([
  "https://app.example.com",
  "https://admin.example.com"
]);

app.use(cors({
  origin(origin, cb) {
    if (!origin) return cb(null, true);
    if (allowedOrigins.has(origin)) return cb(null, true);
    return cb(new Error("Origin not allowed"));
  },
  credentials: true
}));
```

## Remediation

1. Remove wildcard origins from any credentialed CORS configuration.
2. Build explicit allowlists for known trusted web origins per environment.
3. Validate dynamic origin logic against exact matches, not substring checks.
4. Keep gateway and app-layer CORS behavior consistent and documented.
5. Restrict allowed methods and headers to required minimums.
6. Add tests for preflight and credentialed fetches from trusted/untrusted origins.
7. Monitor rejected origins to detect probing and config drift.
8. Reassess CORS when adding new frontend domains or auth mechanisms.

## Verification

- Send credentialed requests from allowed and disallowed origins; verify behavior.
- Confirm responses never include `*` with credentials enabled.
- Validate preflight responses include only expected methods/headers.
- Test browser behavior with real `fetch(..., { credentials: "include" })`.
- Review gateway response headers in production, not just local dev.

## False Positives and Exceptions

- Non-browser clients where CORS headers are irrelevant to access control
- Public, fully unauthenticated read-only APIs not using credentials
- Local development permissive origins, if isolated from production configs
- Strictly internal tools with network isolation and documented risk acceptance

## Related Rules

- `TG-AUTH-004-insecure-session-cookie.md`
- `TG-AUTH-002-client-only-authorization.md`
- `TG-PLATFORM-002-missing-security-headers.md`
