# TG-RATE-002: Unlimited Public Write Endpoint

## Severity

Medium

## Applies To

- Contact forms and feedback submission routes
- Newsletter signup and waitlist endpoints
- Anonymous content creation or comment endpoints
- Webhooks that accept unauthenticated internet traffic
- Any expensive POST/PUT/PATCH endpoint callable pre-auth

## Why It Matters

Public write endpoints are common abuse entry points.
Attackers can flood storage, queues, email providers, and notification systems.
Abuse may not be data theft, but can still create real cost and downtime.
Spam and bot traffic can also degrade analytics and operational trust.
Unchecked write volume becomes an easy denial-of-wallet vector.

## What TorusGuard Looks For

- Unauthenticated write handlers without route-level throttling
- Missing CAPTCHA or bot challenge on high-abuse forms
- No IP, device, or fingerprint-based submission controls
- No duplicate submission detection for identical payloads
- Lack of queue depth or outbound provider safeguards after intake
- Public webhooks with no signature check plus no request limits

## Unsafe Example

```ts
app.post("/api/contact", async (req, res) => {
  await db.contactMessage.create({
    data: {
      email: req.body.email,
      message: req.body.message
    }
  });

  await mailer.send({
    to: "support@example.com",
    subject: "New contact request",
    text: req.body.message
  });

  res.status(201).json({ ok: true });
});
```

## Safe Example

```ts
import rateLimit from "express-rate-limit";

const publicWriteLimiter = rateLimit({
  windowMs: 10 * 60 * 1000,
  max: 20,
  message: { error: "Too many submissions. Please retry later." },
  standardHeaders: true,
  legacyHeaders: false
});

app.post("/api/contact", publicWriteLimiter, async (req, res) => {
  if (!req.body.captchaToken || !(await captcha.verify(req.body.captchaToken))) {
    return res.status(400).json({ error: "Bot challenge failed" });
  }

  await db.contactMessage.create({
    data: { email: req.body.email, message: req.body.message }
  });
  res.status(201).json({ ok: true });
});
```

## Remediation

1. Inventory all anonymous or pre-auth write endpoints.
2. Add route-specific rate limits with lower thresholds than authenticated APIs.
3. Add anti-automation controls (CAPTCHA, proof-of-work, or managed bot defense).
4. Deduplicate repeated payloads to reduce spam amplification.
5. Gate downstream expensive actions (email, SMS, AI calls) with quotas.
6. Enforce signed webhooks where feasible and rate-limit unsigned traffic heavily.
7. Add abuse monitoring dashboards for submission spikes and block decisions.
8. Define an incident playbook for emergency tightening of public write limits.

## Verification

- Send more than allowed form submissions and confirm throttling responses.
- Confirm bot challenge is required and invalid tokens are rejected.
- Verify normal user submission paths remain functional.
- Test downstream providers are not called when requests are throttled.
- Review logs to ensure abuse signals are observable and actionable.

## False Positives and Exceptions

- Endpoint is private behind VPN and not internet-reachable
- Strict gateway quota exists with documented ownership and alerts
- Endpoint is read-mostly and mislabeled as write by route naming only
- Temporary load-test bypass with approved window and post-test rollback

## Related Rules

- `TG-RATE-001-unlimited-auth-endpoint.md`
- `TG-RATE-003-unbounded-resource-consumption.md`
- `TG-INPUT-001-missing-server-validation.md`
- `TG-INPUT-004-unrestricted-file-upload.md`
