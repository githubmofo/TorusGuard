# TG-SEC-001: Hardcoded Secrets in Tracked Source

## Severity
Critical

## Applies To
- JavaScript, TypeScript, Python, Go, Java, C#, Ruby, PHP
- Backend services, scripts, CI helpers, and shared utilities
- Any tracked file in `src/`, `app/`, `server/`, `api/`, `scripts/`, or `lib/`
- Infrastructure manifests that can hold credentials

## Why It Matters
Hardcoded secrets in source control are frequently harvested by automated scanners within minutes of exposure.  
Once committed, credentials may remain accessible through forks, clones, build logs, and historical refs even after removal.  
Leaked API keys, JWT secrets, passwords, and database URLs can enable privilege escalation, data exfiltration, and account takeover.

## What TorusGuard Looks For
- String literals assigned to names such as `apiKey`, `token`, `jwtSecret`, `password`, `dbUrl`, `connectionString`
- Credential-shaped values in code, including:
  - Long base64-like tokens
  - Hex secrets
  - URLs with embedded credentials (`protocol://user:pass@host`)
- Insecure defaults like `JWT_SECRET = "change-me"` left in tracked files
- Commented-out credentials that still exist in committed code
- Secret values in configuration source files (`.ts`, `.js`, `.py`, `.yaml`, `.json`)

## Unsafe Example
```ts
// src/auth/session.ts
import jwt from "jsonwebtoken";

const JWT_SECRET = "prod_jwt_secret_8392b76ed18bb1";
const adminPassword = "S3rv!ce-Adm1n-Temp";
const dbUrl = "postgres://app_user:PlainTextPass@db.internal:5432/payments";

export function signSession(payload: object) {
  return jwt.sign(payload, JWT_SECRET, { expiresIn: "1h" });
}
```

## Safe Example
```ts
// src/auth/session.ts
import jwt from "jsonwebtoken";

const JWT_SECRET = process.env.JWT_SECRET;
const DB_URL = process.env.DATABASE_URL;

if (!JWT_SECRET) {
  throw new Error("Missing JWT_SECRET environment variable");
}

export function signSession(payload: object) {
  return jwt.sign(payload, JWT_SECRET, { expiresIn: "1h" });
}
```

## Remediation (numbered)
1. Remove hardcoded credentials from tracked source files immediately.
2. Move all secrets to environment variables or a managed secrets provider.
3. Rotate every exposed key, password, token, and signing secret.
4. Invalidate active sessions or tokens derived from leaked secrets.
5. Rewrite affected git history if required by policy and incident scope.
6. Add pre-commit and CI secret scanning to prevent recurrence.
7. Document the incident, impact, and completed rotations for auditability.

## Verification
- Search the repository for secret-like assignments and literal credentials.
- Confirm runtime configuration loads from environment or secret manager.
- Validate rotated credentials by checking old values no longer authenticate.
- Review CI and deployment settings to ensure secret injection is externalized.
- Ensure no credential-shaped literals remain in tracked source paths.

## False Positives and Exceptions
- Example/test fixtures are acceptable only when values are obviously fake.
- Non-sensitive identifiers (public analytics IDs, harmless tenant IDs) may match patterns.
- Internal placeholder strings are allowed if they are non-functional and non-deployable.
- Exception approvals should be documented with justification and owner.

## Related Rules
- [TG-SEC-002](./TG-SEC-002-public-environment-secrets.md) - Public environment variable secret exposure
- [TG-SEC-003](./TG-SEC-003-tracked-env-file.md) - Tracked environment file leakage
- [TG-DB-002](./TG-DB-002-privileged-database-credential.md) - Privileged database credentials in browser code
