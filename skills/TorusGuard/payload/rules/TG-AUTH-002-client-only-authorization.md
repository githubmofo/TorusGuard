# TG-AUTH-002: Client-Only Authorization

## Severity
High

## Applies To
- Single-page applications with protected routes
- Mobile apps that hide privileged UI actions
- APIs serving both user and admin clients
- Feature-flagged operations with role constraints

## Why It Matters
Authorization enforced only in frontend code is not security control, because attackers can bypass the UI and call backend APIs directly.
If server endpoints trust client-supplied role flags or hidden form fields, privilege escalation becomes trivial.
Robust authorization must be verified on every sensitive backend action regardless of UI behavior.

## What TorusGuard Looks For
- Admin checks present in frontend components but absent in backend handlers.
- API routes that trust `role`, `isAdmin`, or similar flags from request body/query.
- Hidden buttons/menus used as the only barrier to privileged operations.
- Use of local storage role values for security decisions.
- Missing middleware or policy checks around destructive and high-impact endpoints.

## Unsafe Example
```js
// Frontend blocks non-admin users from seeing delete button
if (currentUser.role === "admin") {
  showDeleteUserButton();
}

// Backend route does not verify authenticated role
app.post("/api/admin/delete-user", async (req, res) => {
  const targetUserId = req.body.userId;
  await db.user.delete({ where: { id: targetUserId } });
  res.json({ ok: true });
});
```

## Safe Example
```js
function requireRole(...allowedRoles) {
  return (req, res, next) => {
    const role = req.auth?.role;
    if (!allowedRoles.includes(role)) {
      return res.status(403).json({ ok: false, error: "Forbidden" });
    }
    next();
  };
}

app.post("/api/admin/delete-user", requireAuth, requireRole("admin"), async (req, res) => {
  const targetUserId = String(req.body.userId || "");
  if (!/^[a-f0-9-]{36}$/.test(targetUserId)) {
    return res.status(400).json({ ok: false, error: "Invalid user id" });
  }

  await db.user.delete({ where: { id: targetUserId } });
  res.json({ ok: true });
});
```

## Remediation
1. Enforce authorization checks on the server for every protected action and resource.
2. Derive roles/permissions from authenticated server-side identity, not request payload flags.
3. Implement centralized policy middleware to reduce inconsistent endpoint protection.
4. Keep frontend role checks for UX only, never as the sole security mechanism.
5. Add audit logging for privileged operations including actor, target, and outcome.
6. Write regression tests that call endpoints directly without using the UI.

## Verification
- Call privileged endpoints with a non-admin token and verify consistent `403` responses.
- Remove/hide frontend restrictions in browser devtools and confirm backend still blocks access.
- Attempt sending forged `isAdmin: true` fields and verify they are ignored.
- Inspect route registrations to ensure protected middleware is applied universally.
- Review audit logs for denied authorization attempts.

## False Positives and Exceptions
- Public metadata endpoints may intentionally skip authorization if they contain no sensitive operations or data.
- Early prototypes often rely on frontend checks; production deployment must not.
- Internal admin APIs still require authorization controls unless isolated by strong network identity boundaries.

## Related Rules
- [TG-AUTH-003](./TG-AUTH-003-missing-object-authorization.md)
- [TG-AUTH-004](./TG-AUTH-004-insecure-session-cookie.md)
- [TG-INPUT-001](./TG-INPUT-001-missing-server-validation.md)
