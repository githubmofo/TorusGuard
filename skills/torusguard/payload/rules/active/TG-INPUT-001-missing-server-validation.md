# TG-INPUT-001: Missing Server-Side Validation

## Severity
High

## Applies To
- REST and GraphQL API handlers
- Form-processing backend endpoints
- Message queue consumers that accept external payloads
- Admin/import endpoints that trust UI validation

## Why It Matters
Client-side checks are easy to bypass because attackers can send crafted requests directly to backend endpoints.
When the server does not validate required fields, data type, length, format, range, and allowed values, malicious input can trigger account takeover paths, integrity failures, and downstream injection vulnerabilities.
Server-side validation is also required to keep business rules enforceable when multiple clients, scripts, and integrations call the same APIs.

## What TorusGuard Looks For
- Request data read from `req.body`, `req.query`, `req.params`, headers, or raw payloads without schema validation.
- Validation done only in frontend files while backend endpoint accepts the same fields blindly.
- Direct persistence of user-provided objects with broad spread operators.
- Type coercion and fallback logic that silently accepts invalid values.
- Missing allowlists for enum-like fields such as role, status, country code, or operation type.

## Unsafe Example
```js
// Express route that trusts client validation
app.post("/api/profile", async (req, res) => {
  const { displayName, age, newsletter, role } = req.body;

  // No server-side validation:
  // - displayName could be extremely long or contain control chars
  // - age could be negative or non-numeric
  // - newsletter could be arbitrary string
  // - role could be escalated to "admin"
  const updated = await db.user.update({
    where: { id: req.user.id },
    data: { displayName, age, newsletter, role }
  });

  res.json({ ok: true, user: updated });
});
```

## Safe Example
```js
import { z } from "zod";

const updateProfileSchema = z.object({
  displayName: z.string().min(2).max(60).regex(/^[a-zA-Z0-9 _.-]+$/),
  age: z.number().int().min(13).max(120),
  newsletter: z.boolean(),
  role: z.enum(["user"]) // client cannot self-assign privileged roles
});

app.post("/api/profile", async (req, res) => {
  const parsed = updateProfileSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({
      ok: false,
      error: "Invalid input",
      details: parsed.error.issues
    });
  }

  const { displayName, age, newsletter } = parsed.data;
  const updated = await db.user.update({
    where: { id: req.user.id },
    data: { displayName, age, newsletter }
  });

  res.json({ ok: true, user: updated });
});
```

## Remediation
1. Define strict server-side schemas for every externally reachable input surface.
2. Validate before business logic, authorization decisions, and database writes.
3. Enforce field allowlists; reject unexpected keys rather than silently ignoring them.
4. Apply normalization after validation (trim, case-fold, canonical forms) where needed.
5. Centralize reusable validators for shared payloads to prevent drift across endpoints.
6. Return clear but non-sensitive validation errors, and log rejection metrics for monitoring.

## Verification
- Send malformed payloads directly with `curl` or API clients, bypassing the web UI.
- Confirm invalid types, out-of-range values, and unknown fields return `400`.
- Attempt privilege-related field tampering and verify values are rejected or ignored safely.
- Run integration tests covering boundary values and negative cases.
- Ensure validation runs for all entry paths, including batch/import and background worker routes.

## False Positives and Exceptions
- Internal service-to-service endpoints may appear unvalidated but can be acceptable if strong contract validation is enforced at the gateway and mutual trust boundaries are documented.
- Auto-generated API frameworks sometimes perform implicit validation; keep explicit schema definitions for auditability.
- Legacy endpoints under migration can be temporarily exempted only with compensating controls and a tracked deprecation timeline.

## Related Rules
- [TG-INPUT-002](./TG-INPUT-002-raw-sql-concatenation.md)
- [TG-INPUT-003](./TG-INPUT-003-unsafe-html-or-code-execution.md)
- [TG-AUTH-003](./TG-AUTH-003-missing-object-authorization.md)
