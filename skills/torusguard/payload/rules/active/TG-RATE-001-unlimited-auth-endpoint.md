# TG-RATE-001: Unlimited Authentication Endpoint

## Severity

High

## Applies To

- Login endpoints (`/login`, `/signin`, `/api/auth/login`)
- Password reset request endpoints
- OTP and magic-link request endpoints
- Token exchange and refresh endpoints exposed to internet clients

## Why It Matters

Authentication surfaces are high-value brute-force targets.
Without request throttling, attackers can attempt large credential lists quickly.
Even with strong password hashing, unlimited retries can cause account takeover.
Unauthenticated auth endpoints are also cheap to hit from botnets.
Excessive failures can degrade performance and create noisy logs.
Credential stuffing campaigns usually start here before lateral abuse.

## What TorusGuard Looks For

- Auth route handlers with no middleware or logic that tracks attempts
- No dependency usage for rate limiting (`express-rate-limit`, Redis counters, gateway policies)
- Missing per-identity or per-IP backoff decisions on failed auth
- Password reset or OTP endpoints callable repeatedly without cooldown
- Comments or TODOs that acknowledge rate limiting is not implemented
- Reverse proxy configs that do not define request limits for auth paths

## Unsafe Example

```ts
import express from "express";
import { verifyPassword } from "./auth";

const app = express();
app.use(express.json());

app.post("/api/auth/login", async (req, res) => {
  const { email, password } = req.body;
  const user = await db.user.findUnique({ where: { email } });

  if (!user || !(await verifyPassword(password, user.passwordHash))) {
    return res.status(401).json({ error: "Invalid credentials" });
  }

  return res.json({ token: signJwt({ sub: user.id }) });
});
```

## Safe Example

```ts
import express from "express";
import rateLimit from "express-rate-limit";
import { verifyPassword } from "./auth";

const app = express();
app.use(express.json());

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 10,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: "Too many authentication attempts. Try later." }
});

app.post("/api/auth/login", authLimiter, async (req, res) => {
  const { email, password } = req.body;
  const user = await db.user.findUnique({ where: { email } });
  if (!user || !(await verifyPassword(password, user.passwordHash))) {
    return res.status(401).json({ error: "Invalid credentials" });
  }
  return res.json({ token: signJwt({ sub: user.id }) });
});
```

## Remediation

1. Identify every internet-facing authentication and account-recovery endpoint.
2. Apply a rate limiter at app, gateway, or CDN edge for those routes.
3. Add tighter thresholds for auth than for generic API traffic.
4. Layer controls: per-IP + per-account/email counters when possible.
5. Introduce cooldown/backoff after repeated failures.
6. Return uniform auth errors to avoid account enumeration.
7. Ensure limits are distributed (Redis or gateway), not in-process only.
8. Alert on sustained throttling spikes as potential credential-stuffing.

## Verification

- Trigger more than allowed login failures from a single source and confirm `429`.
- Confirm `Retry-After` or equivalent response hints are present.
- Validate successful logins still work under normal user behavior.
- Verify limits apply to reset, OTP, and magic-link request endpoints too.
- Inspect deployment gateway/WAF config to ensure parity with app behavior.

## False Positives and Exceptions

- Internal service-to-service auth endpoints behind private network controls only
- Endpoints already protected by managed API gateway quotas with strict scopes
- Staging environments used only in private CI where public traffic is impossible
- Temporary elevated limits during controlled load tests (must be time-boxed)

## Related Rules

- `TG-AUTH-005-unsafe-password-reset.md`
- `TG-AUTH-001-weak-password-storage.md`
- `TG-RATE-002-unlimited-public-write-endpoint.md`
- `TG-RATE-003-unbounded-resource-consumption.md`
