# TG-PLATFORM-002: Missing Security Headers

## Severity

Medium

## Applies To

- Node/Express/Nest/Fastify web apps serving browser traffic
- Reverse proxies and CDN layers terminating TLS
- SSR frontends and static sites with custom response headers
- APIs returning HTML, login pages, docs portals, or admin consoles
- Deployments expected to enforce baseline browser hardening

## Why It Matters

Security headers reduce exploitability of common web attack classes.
Missing headers increase risk from XSS, clickjacking, protocol downgrade, and data leakage.
Headers are not complete protection, but are critical platform defense-in-depth.
Gaps often appear during framework migrations or proxy reconfiguration.
A weak default posture compounds impact of unrelated code bugs.

## What TorusGuard Looks For

- Absent or weak `Content-Security-Policy` on HTML responses
- Missing `Strict-Transport-Security` on HTTPS production domains
- Missing `X-Frame-Options` or equivalent `frame-ancestors` directive
- Missing `X-Content-Type-Options: nosniff`
- No `Referrer-Policy` or overly permissive values
- Express apps not using Helmet (or equivalent explicit header strategy)

## Unsafe Example

```ts
import express from "express";
const app = express();

app.get("/", (_req, res) => {
  res.sendFile("index.html");
});
```

## Safe Example

```ts
import express from "express";
import helmet from "helmet";

const app = express();

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      objectSrc: ["'none'"],
      frameAncestors: ["'none'"],
      upgradeInsecureRequests: []
    }
  },
  hsts: { maxAge: 31536000, includeSubDomains: true, preload: true }
}));
```

## Remediation

1. Define a minimum security header baseline for all browser-facing responses.
2. Enable `helmet` (or equivalent) and customize CSP for app-specific needs.
3. Enforce HSTS only on HTTPS production domains with rollout planning.
4. Add `X-Content-Type-Options`, frame protections, and sane referrer policy.
5. Move inline scripts/styles to nonce/hash-based CSP-compatible patterns.
6. Validate header behavior at proxy/CDN and app layers to avoid overwrites.
7. Add automated tests or synthetic checks for required headers per route type.
8. Document approved exceptions for legacy integrations and review periodically.

## Verification

- Inspect response headers on HTML routes in production.
- Confirm CSP blocks inline/eval behavior unless explicitly allowed.
- Validate HSTS appears only on HTTPS and matches intended max-age/preload policy.
- Test clickjacking protections with iframe embedding attempts.
- Run security scanner checks and verify no regressions after deploy.

## False Positives and Exceptions

- Pure JSON internal APIs not rendered in browsers (still consider baseline headers)
- Development environments where CSP is relaxed for hot reload tooling
- Legacy pages requiring transitional CSP policies during migration windows
- Routes intentionally embeddable by trusted partners with explicit frame policy docs

## Related Rules

- `TG-PLATFORM-001-wildcard-cors-with-credentials.md`
- `TG-PLATFORM-003-production-stack-trace-exposure.md`
- `TG-INPUT-003-unsafe-html-or-code-execution.md`
