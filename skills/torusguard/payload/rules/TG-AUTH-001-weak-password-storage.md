# TG-AUTH-001: Weak Password Storage

## Severity
Critical

## Applies To
- User registration and login systems
- Password reset and credential update flows
- Legacy account import/migration jobs
- Identity providers that store local credentials

## Why It Matters
Weak password storage enables catastrophic compromise when databases leak through attacks, backups, logs, or insider misuse.
Plaintext, reversible encryption, or fast unsalted hashes let attackers recover passwords quickly and reuse them across services.
Secure, adaptive hashing with per-password salt and optional pepper drastically reduces offline cracking feasibility.

## What TorusGuard Looks For
- Passwords stored as plaintext or encoded forms such as Base64.
- Use of outdated fast hashes (`MD5`, `SHA1`, bare `SHA256`) for password storage.
- Same hash value for identical passwords due to missing random salt.
- Manual cryptography routines instead of vetted password hashing libraries.
- Logging of raw passwords or hash inputs during authentication workflows.

## Unsafe Example
```js
import crypto from "crypto";

app.post("/api/register", async (req, res) => {
  const email = req.body.email;
  const password = req.body.password;

  // Fast hash with no salt and no work factor
  const passwordHash = crypto.createHash("sha256").update(password).digest("hex");

  await db.user.create({
    data: { email, password_hash: passwordHash }
  });

  res.json({ ok: true });
});
```

## Safe Example
```js
import argon2 from "argon2";

app.post("/api/register", async (req, res) => {
  const email = String(req.body.email || "");
  const password = String(req.body.password || "");

  if (password.length < 12) {
    return res.status(400).json({ ok: false, error: "Password too short" });
  }

  const hash = await argon2.hash(password, {
    type: argon2.argon2id,
    memoryCost: 19456,
    timeCost: 2,
    parallelism: 1
  });

  await db.user.create({
    data: { email, password_hash: hash }
  });

  res.json({ ok: true });
});

app.post("/api/login", async (req, res) => {
  const user = await db.user.findUnique({ where: { email: req.body.email } });
  if (!user) return res.status(401).json({ ok: false });

  const valid = await argon2.verify(user.password_hash, String(req.body.password || ""));
  if (!valid) return res.status(401).json({ ok: false });

  res.json({ ok: true });
});
```

## Remediation
1. Replace insecure password storage with Argon2id, bcrypt, or scrypt using recommended cost factors.
2. Ensure each password hash includes a unique random salt (handled by modern libraries).
3. Add optional application-level pepper stored in a secret manager, not in the database.
4. Remove password values from logs, traces, analytics events, and error telemetry.
5. Migrate existing hashes using rehash-on-login or controlled reset campaigns.
6. Periodically tune work factors based on current hardware and latency targets.

## Verification
- Inspect stored credential records and confirm they use adaptive hash formats.
- Verify identical passwords across test accounts produce different hash outputs.
- Benchmark login flow to ensure configured cost factors are actually applied.
- Attempt cracking tests on sample exported hashes to validate resistance assumptions.
- Review codebase for direct use of fast hash APIs in authentication modules.

## False Positives and Exceptions
- One-way hashes for non-password tokens may look similar but are separate controls.
- Temporary test fixtures can include static hashes only if isolated from production data paths.
- External identity providers reduce local password handling scope but do not exempt backup credential paths.

## Related Rules
- [TG-AUTH-005](./TG-AUTH-005-unsafe-password-reset.md)
- [TG-AUTH-004](./TG-AUTH-004-insecure-session-cookie.md)
- [TG-INPUT-001](./TG-INPUT-001-missing-server-validation.md)
