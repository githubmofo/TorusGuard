# TG-CLIENT-002: Sensitive Client Bundle Content

## Severity

High

## Applies To

- Frontend JavaScript/TypeScript bundles shipped to browsers
- React, Next.js, Vite, CRA, and other web client builds
- Client logs (`console.log`, telemetry breadcrumbs, debug overlays)
- Embedded config constants and generated runtime environment payloads
- Source files that may be tree-shaken incorrectly but still leak literals

## Why It Matters

Anything shipped to the browser is attacker-accessible by design.
Secrets, tokens, admin keys, or internal endpoints in bundles are effectively public.
Sensitive debug logs can leak credentials into screenshots and support tickets.
A single hardcoded secret can enable direct backend or third-party API compromise.
This is a high-impact exposure class and often immediately exploitable.
Browser DevTools cannot be blocked, so any client-shipped secret should be treated as compromised.

## What TorusGuard Looks For

- Hardcoded API keys, bearer tokens, private keys, or signing secrets in client code
- Usage of server-only env vars in frontend modules
- `console.log`/`console.debug` outputting JWTs, session tokens, or PII
- Debug utilities that serialize auth headers or full user objects in production
- References to admin-only endpoints from unauthenticated client paths
- Bundle artifacts containing known secret patterns or credential-like strings

## Unsafe Example

```ts
// src/api/client.ts
const ADMIN_TOKEN = "sk_live_9f2a...supersecret";

export async function createInvoice(payload: unknown) {
  console.log("using token", ADMIN_TOKEN);
  return fetch("https://api.example.com/admin/invoices", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${ADMIN_TOKEN}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });
}
```

## Safe Example

```ts
// src/api/client.ts
export async function createInvoice(payload: unknown) {
  return fetch("/api/invoices", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}

// server route uses server-side credentials only
app.post("/api/invoices", requireAuth, async (req, res) => {
  const result = await billing.createInvoice(req.user.id, req.body);
  res.json(result);
});
```

## Remediation

1. Remove all secrets and privileged tokens from client code and build-time env payloads.
2. Move privileged API calls behind server endpoints with proper authz checks.
3. Restrict frontend env variables to explicitly public-safe values only.
4. Strip sensitive console statements in production builds.
5. Add CI secret scanning for source and compiled bundles.
6. Rotate any leaked credentials immediately and revoke prior tokens.
7. Add code review gates that block server-only value usage in client modules.
8. Educate teams that browser code is always inspectable by users and attackers.

## Verification

- Inspect built bundles and search for token/key patterns and internal secrets.
- Run app in production mode and confirm no sensitive console output.
- Verify privileged operations require server-mediated authentication and authorization.
- Validate rotated credentials are active and leaked values are revoked.
- Confirm public env allowlist is enforced in CI/build scripts.

## False Positives and Exceptions

- Public publishable keys intentionally designed for client use (documented by vendor)
- Fake/sample credentials used only in local demo code outside production builds
- Debug logs in non-production branches that are stripped before release
- Internal tools with private distribution, if risk accepted explicitly

## Related Rules

- `TG-SEC-001-hardcoded-secrets.md`
- `TG-SEC-002-public-environment-secrets.md`
- `TG-CLIENT-001-public-production-source-maps.md`
- `TG-AUTH-002-client-only-authorization.md`
