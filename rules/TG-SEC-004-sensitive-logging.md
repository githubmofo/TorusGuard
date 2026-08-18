# TG-SEC-004: Sensitive Information in Logs

## Severity
Medium

## Applies To
- Application logs in backend services, workers, and serverless functions
- Client-side error logging and telemetry pipelines
- Authentication middleware and API gateway handlers
- Structured logs, plaintext logs, and third-party observability sinks

## Why It Matters
Logs are broadly distributed across systems, retained for long periods, and frequently accessible to many operators.  
If passwords, tokens, cookies, or authorization headers are logged, sensitive data can be replayed or abused.  
Log leakage often bypasses normal secret handling controls because it happens after request processing.

## What TorusGuard Looks For
- Direct logging of request bodies containing credentials
- Logging of headers without redaction, especially `Authorization` and `Cookie`
- Serialization of auth/session objects that include tokens
- Error logs that concatenate secret values into exception messages
- Debug statements printing plaintext passwords, OTP codes, or API keys

## Unsafe Example
```ts
// src/middleware/login.ts
export async function loginHandler(req, res) {
  console.info("Login payload", req.body);
  console.info("Auth header", req.headers.authorization);

  const token = await issueToken(req.body.email);
  console.debug(`issued token=${token}`);
  return res.json({ ok: true });
}
```

## Safe Example
```ts
// src/middleware/login.ts
function redactAuthHeader(value?: string) {
  if (!value) return "missing";
  return value.startsWith("Bearer ") ? "Bearer [REDACTED]" : "[REDACTED]";
}

export async function loginHandler(req, res) {
  console.info("Login attempt", {
    emailDomain: req.body.email?.split("@")[1] ?? "unknown",
    hasPassword: Boolean(req.body.password),
    auth: redactAuthHeader(req.headers.authorization),
  });

  const token = await issueToken(req.body.email);
  console.debug("Issued session token", { token: "[REDACTED]" });
  return res.json({ ok: true });
}
```

## Remediation (numbered)
1. Remove direct logging of request bodies and sensitive headers.
2. Implement centralized redaction for known secret fields and header keys.
3. Log metadata and security-relevant context without raw secret values.
4. Update logging wrappers to block unsafe keys by default.
5. Rotate credentials if logs already captured valid sensitive data.
6. Restrict log access and retention for security-sensitive services.
7. Add automated tests to assert redaction behavior in logging utilities.

## Verification
- Search logging calls for `password`, `token`, `authorization`, and `cookie` fields.
- Generate representative requests and inspect emitted logs for redaction.
- Confirm tracing/telemetry exporters do not reintroduce sensitive attributes.
- Validate historical logs for recent exposure and incident follow-up needs.
- Ensure secure logging guidance is included in service development standards.

## False Positives and Exceptions
- Logging token hashes or irreversible fingerprints may be acceptable for correlation.
- Masked values can still trigger detections; confirm full redaction depth.
- Security incident forensics may require temporary enhanced logs under strict controls.
- Exceptions must include expiration, owner, and explicit approval.

## Related Rules
- [TG-SEC-001](./TG-SEC-001-hardcoded-secrets.md) - Source-level hardcoded secret exposure
- [TG-SEC-003](./TG-SEC-003-tracked-env-file.md) - Secret leakage through tracked env files
- [TG-DB-002](./TG-DB-002-privileged-database-credential.md) - Privileged credentials exposed to clients
