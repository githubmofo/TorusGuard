# TG-AUTH-003: Missing Object-Level Authorization (IDOR)

## Severity
High

## Applies To
- APIs that fetch or modify records by ID
- File and document retrieval endpoints
- Multi-tenant systems with organization-scoped data
- Billing, messaging, and profile management resources

## Why It Matters
IDOR occurs when applications expose object identifiers but fail to verify that the requester is allowed to access that specific object.
Attackers can enumerate or guess IDs to read, modify, or delete other users' resources without needing elevated roles.
This creates severe confidentiality and integrity breaches, especially in multi-tenant products.

## What TorusGuard Looks For
- Endpoints reading `:id` or query IDs without ownership or tenant checks.
- `findUnique`/`getById` calls that do not include current user or tenant constraints.
- Access to files/records based solely on untrusted identifier parameters.
- Sequential numeric IDs exposed in URLs with missing authorization guards.
- Update/delete operations that authenticate user identity but skip object-level policy.

## Unsafe Example
```js
app.get("/api/invoices/:invoiceId", requireAuth, async (req, res) => {
  const invoiceId = req.params.invoiceId;

  // Authenticated, but no check that invoice belongs to this user/tenant
  const invoice = await db.invoice.findUnique({
    where: { id: invoiceId }
  });

  if (!invoice) return res.status(404).json({ ok: false });
  res.json({ ok: true, invoice });
});
```

## Safe Example
```js
app.get("/api/invoices/:invoiceId", requireAuth, async (req, res) => {
  const invoiceId = String(req.params.invoiceId || "");
  const userId = req.auth.userId;
  const tenantId = req.auth.tenantId;

  const invoice = await db.invoice.findFirst({
    where: {
      id: invoiceId,
      tenant_id: tenantId,
      customer_user_id: userId
    }
  });

  if (!invoice) {
    return res.status(404).json({ ok: false, error: "Not found" });
  }

  res.json({ ok: true, invoice });
});
```

## Remediation
1. Apply object-level authorization checks on every read, update, and delete path.
2. Scope data queries by authenticated user, tenant, account, or policy context.
3. Centralize authorization policies so object checks are consistent across endpoints.
4. Avoid exposing predictable identifiers when not required; consider opaque IDs.
5. Log access denials and anomalous ID probing attempts for detection.
6. Add tests that attempt cross-user and cross-tenant access with valid credentials.

## Verification
- Authenticate as User A and request User B resources by changing IDs.
- Confirm unauthorized object access returns `404` or `403` consistently without data leakage.
- Test update and delete endpoints, not only read endpoints.
- Validate background jobs and export endpoints enforce tenant/object constraints too.
- Inspect ORM/database queries for required ownership predicates.

## False Positives and Exceptions
- Public resources intentionally shared across tenants should be explicitly labeled and policy-reviewed.
- Some administrative roles can access cross-tenant objects, but this must be explicit and auditable.
- Random UUID usage alone does not remove need for object authorization.

## Related Rules
- [TG-AUTH-002](./TG-AUTH-002-client-only-authorization.md)
- [TG-INPUT-001](./TG-INPUT-001-missing-server-validation.md)
- [TG-INPUT-002](./TG-INPUT-002-raw-sql-concatenation.md)
