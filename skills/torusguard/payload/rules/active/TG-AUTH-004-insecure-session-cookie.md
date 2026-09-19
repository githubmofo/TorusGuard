# TG-AUTH-004: Insecure Session Cookie Configuration

## Severity
High

## Applies To
- Web applications using cookie-based sessions
- Authentication gateways and reverse proxies
- Legacy apps migrating from token storage in local storage
- SSO callback handlers setting auth cookies

## Why It Matters
Session cookies that lack secure attributes can be stolen, replayed, or manipulated by attackers.
Missing `HttpOnly` enables JavaScript access during XSS, missing `Secure` exposes cookies over unencrypted transport, and weak `SameSite` settings increase CSRF risk.
Improper domain/path/lifetime settings also expand token exposure across subdomains and long time windows.

## What TorusGuard Looks For
- Cookies set without `HttpOnly`, `Secure`, or explicit `SameSite`.
- Session identifiers in URL parameters or local storage instead of hardened cookies.
- Excessive cookie lifetime for sensitive sessions.
- Broad cookie domain scopes (`.example.com`) without necessity.
- Session rotation missing after login, privilege change, or password reset.

## Unsafe Example
```js
app.post("/api/login", async (req, res) => {
  const sessionId = await createSession(req.body.email, req.body.password);
  if (!sessionId) return res.status(401).json({ ok: false });

  // Missing critical security attributes
  res.cookie("sid", sessionId, {
    sameSite: "none"
  });

  res.json({ ok: true });
});
```

## Safe Example
```js
app.post("/api/login", async (req, res) => {
  const user = await verifyCredentials(req.body.email, req.body.password);
  if (!user) return res.status(401).json({ ok: false });

  const sessionId = await createSession(user.id);
  res.cookie("sid", sessionId, {
    httpOnly: true,
    secure: true,
    sameSite: "lax",
    path: "/",
    maxAge: 1000 * 60 * 30 // 30 minutes
  });

  res.json({ ok: true });
});

app.post("/api/password/reset/complete", requireAuth, async (req, res) => {
  await invalidateAllSessions(req.auth.userId);
  const rotated = await createSession(req.auth.userId);

  res.cookie("sid", rotated, {
    httpOnly: true,
    secure: true,
    sameSite: "strict",
    path: "/",
    maxAge: 1000 * 60 * 15
  });

  res.json({ ok: true });
});
```

## Remediation
1. Set `HttpOnly`, `Secure`, and explicit `SameSite` on all session/auth cookies.
2. Use HTTPS everywhere; reject insecure origins and mixed-content session transport.
3. Minimize cookie scope with narrow domain/path and reasonable expiration.
4. Rotate session IDs on authentication, privilege transitions, and credential recovery.
5. Invalidate old sessions on logout, password changes, and suspicious activity.
6. Add CSRF protections compatible with cookie strategy for state-changing requests.

## Verification
- Inspect `Set-Cookie` headers in browser/network tools for required attributes.
- Attempt JavaScript cookie reads and confirm auth cookies are inaccessible.
- Test login over HTTP in non-production environments and ensure secure policy behavior.
- Validate old session IDs stop working after rotation events.
- Confirm cross-site POST attempts are blocked by SameSite and CSRF controls.

## False Positives and Exceptions
- `SameSite=None` can be valid for specific cross-site SSO flows, but requires `Secure` and additional CSRF controls.
- Development environments on localhost may need adjusted secure handling; document separation from production settings.
- Stateless bearer tokens in headers are out of scope for this rule but require equivalent protections.

## Related Rules
- [TG-AUTH-002](./TG-AUTH-002-client-only-authorization.md)
- [TG-AUTH-005](./TG-AUTH-005-unsafe-password-reset.md)
- [TG-INPUT-003](./TG-INPUT-003-unsafe-html-or-code-execution.md)
