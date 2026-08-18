# TG-PLATFORM-003: Production Stack Trace Exposure

## Severity

Medium

## Applies To

- API error handlers and exception middleware
- SSR frameworks rendering error pages
- Reverse proxies returning upstream crash output
- Serverless functions with default runtime error responses
- Any production system handling untrusted request input

## Why It Matters

Verbose errors leak internal details useful to attackers.
Stack traces can expose file paths, package versions, SQL snippets, and infrastructure hints.
These details speed exploitation and reduce attacker guesswork.
Operationally, noisy error disclosures also increase user confusion.
Secure systems return minimal client-facing errors while preserving server-side diagnostics.

## What TorusGuard Looks For

- `res.status(500).send(err.stack)` or equivalent direct stack output
- Framework debug mode enabled in production (`NODE_ENV` misconfiguration)
- Error pages rendering exception messages and traces to all users
- Serialized internal exception objects returned in JSON responses
- Unhandled promise rejections bubbling raw runtime traces to clients
- Proxy settings forwarding upstream debug bodies externally

## Unsafe Example

```ts
app.use((err, _req, res, _next) => {
  console.error(err);
  res.status(500).json({
    message: err.message,
    stack: err.stack,
    details: err
  });
});
```

## Safe Example

```ts
app.use((err, req, res, _next) => {
  logger.error({
    path: req.path,
    method: req.method,
    errorName: err.name,
    message: err.message,
    stack: err.stack
  });

  res.status(500).json({
    error: "Internal server error",
    requestId: req.id
  });
});
```

## Remediation

1. Implement centralized error handling that returns generic client messages.
2. Log full diagnostics server-side only, including correlation IDs.
3. Disable framework debug/error overlays in production builds.
4. Normalize known operational errors to safe, minimal response schemas.
5. Ensure proxies and serverless gateways do not leak upstream traces.
6. Add secure defaults for unhandled rejections and uncaught exceptions.
7. Review third-party middleware for verbose error serialization behavior.
8. Include incident drill checks for accidental debug-mode deployment.

## Verification

- Trigger representative 500 errors and inspect client responses for leakage.
- Confirm stack traces appear in structured logs, not in API bodies.
- Validate production config disables debug pages/overlays.
- Test SSR routes and static error pages for internal path/version exposure.
- Run dynamic scans searching for stack signatures in responses.

## False Positives and Exceptions

- Authenticated internal observability endpoints restricted to operators
- Short-lived canary diagnostics behind strict access controls
- Non-production environments clearly isolated from public traffic
- Sanitized error messages that include only non-sensitive validation metadata

## Related Rules

- `TG-PLATFORM-002-missing-security-headers.md`
- `TG-INPUT-001-missing-server-validation.md`
- `TG-SEC-004-sensitive-logging.md`
