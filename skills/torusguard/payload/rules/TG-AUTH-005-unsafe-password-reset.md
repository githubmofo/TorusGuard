# TG-AUTH-005: Unsafe Password Reset Flow

## Severity
High

## Applies To
- "Forgot password" and account recovery endpoints
- Email/SMS reset token issuance and verification
- Self-service credential recovery in web and mobile apps
- Administrative reset tooling for user accounts

## Why It Matters
Password reset is a high-value account takeover target because it bypasses existing credentials.
Weak reset token generation, leakage through URLs/logs, missing expiry, and lack of rate limiting can let attackers hijack accounts at scale.
Unsafe reset completion logic can also leave existing sessions active, preserving attacker access.

## What TorusGuard Looks For
- Predictable reset tokens or short numeric codes without brute-force protection.
- Reset tokens stored in plaintext and compared directly.
- Missing token expiry, single-use enforcement, or account binding checks.
- User enumeration through distinct responses for existing vs non-existing emails.
- Failure to invalidate active sessions after successful password reset.

## Unsafe Example
```js
app.post("/api/password/forgot", async (req, res) => {
  const user = await db.user.findUnique({ where: { email: req.body.email } });
  if (!user) return res.status(404).json({ ok: false, error: "No account found" });

  const token = Math.floor(Math.random() * 1000000).toString();
  await db.password_reset.create({
    data: { user_id: user.id, token, expires_at: null, used: false }
  });

  await sendMail(user.email, `Reset link: https://app.example/reset?token=${token}`);
  res.json({ ok: true });
});
```

## Safe Example
```js
import crypto from "crypto";

app.post("/api/password/forgot", async (req, res) => {
  const email = String(req.body.email || "").toLowerCase();
  const user = await db.user.findUnique({ where: { email } });

  // Always return generic response to prevent user enumeration
  if (user) {
    const rawToken = crypto.randomBytes(32).toString("hex");
    const tokenHash = crypto.createHash("sha256").update(rawToken).digest("hex");
    const expiresAt = new Date(Date.now() + 15 * 60 * 1000);

    await db.password_reset.create({
      data: { user_id: user.id, token_hash: tokenHash, expires_at: expiresAt, used: false }
    });

    await sendMail(user.email, `Reset link: https://app.example/reset?token=${rawToken}`);
  }

  res.json({ ok: true, message: "If an account exists, a reset email has been sent." });
});

app.post("/api/password/reset", async (req, res) => {
  const rawToken = String(req.body.token || "");
  const newPassword = String(req.body.newPassword || "");
  const tokenHash = crypto.createHash("sha256").update(rawToken).digest("hex");

  const record = await db.password_reset.findFirst({
    where: { token_hash: tokenHash, used: false, expires_at: { gt: new Date() } }
  });
  if (!record) return res.status(400).json({ ok: false, error: "Invalid or expired token" });

  await setUserPassword(record.user_id, newPassword);
  await db.password_reset.update({ where: { id: record.id }, data: { used: true } });
  await invalidateAllSessions(record.user_id);
  res.json({ ok: true });
});
```

## Remediation
1. Generate cryptographically strong, high-entropy reset tokens and store only token hashes.
2. Enforce short token lifetime, one-time use, and strict account binding.
3. Apply rate limits and anomaly detection on reset request and token verification endpoints.
4. Return generic responses for reset initiation to prevent account enumeration.
5. Invalidate active sessions and recovery artifacts after successful password reset.
6. Require strong new passwords and optionally step-up verification for risky reset attempts.

## Verification
- Request reset for known and unknown emails; verify indistinguishable responses.
- Attempt brute-force token guesses and confirm lockout/rate-limit behavior.
- Reuse a consumed token and confirm it fails.
- Use an expired token and verify rejection path.
- Confirm all existing sessions are invalidated after reset completion.

## False Positives and Exceptions
- Enterprise SSO environments may delegate password reset externally; local reset flows should be disabled or strongly gated.
- Short OTP codes can be acceptable when combined with strict attempt limits, device binding, and very short expiry.
- Manual support resets need controlled operator workflows and audit trails.

## Related Rules
- [TG-AUTH-001](./TG-AUTH-001-weak-password-storage.md)
- [TG-AUTH-004](./TG-AUTH-004-insecure-session-cookie.md)
- [TG-INPUT-001](./TG-INPUT-001-missing-server-validation.md)
