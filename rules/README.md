# TorusGuard Rule Catalog

Stable rule IDs for TorusGuard v0.2.0. Each rule has a dedicated document in this directory.

## Severity Definitions

| Severity | Meaning |
|----------|---------|
| **Critical** | Secret exposure or flaw enabling immediate compromise of sensitive systems/data |
| **High** | Exploitable weakness likely to expose or modify sensitive data, accounts, or privileged operations |
| **Medium** | Important defense gap with meaningful but contextual impact |
| **Low** | Hardening improvement or limited direct impact |
| **Info** | Best-practice observation requiring human judgment |

## Rule Index

### Secrets and Configuration

| ID | Title | Default Severity |
|----|-------|------------------|
| [TG-SEC-001](TG-SEC-001-hardcoded-secrets.md) | Hardcoded Secret | Critical |
| [TG-SEC-002](TG-SEC-002-public-environment-secrets.md) | Sensitive Value in Public Environment Variable | Critical |
| [TG-SEC-003](TG-SEC-003-tracked-env-file.md) | Tracked Environment File | High |
| [TG-SEC-004](TG-SEC-004-sensitive-logging.md) | Sensitive Data Logging | Medium |

### Frontend Database Exposure

| ID | Title | Default Severity |
|----|-------|------------------|
| [TG-DB-001](TG-DB-001-frontend-database-query.md) | Database Query in Frontend Source | High |
| [TG-DB-002](TG-DB-002-privileged-database-credential.md) | Privileged Database Credential in Browser Code | Critical |
| [TG-DB-003](TG-DB-003-frontend-admin-sdk.md) | Frontend Admin SDK or Privileged Client | Critical |

### Input and Injection

| ID | Title | Default Severity |
|----|-------|------------------|
| [TG-INPUT-001](TG-INPUT-001-missing-server-validation.md) | Missing Server-Side Input Validation | High |
| [TG-INPUT-002](TG-INPUT-002-raw-sql-concatenation.md) | Raw SQL Concatenation | Critical |
| [TG-INPUT-003](TG-INPUT-003-unsafe-html-or-code-execution.md) | Unsafe HTML or Dynamic Code Execution | High |
| [TG-INPUT-004](TG-INPUT-004-unrestricted-file-upload.md) | Unrestricted File Upload | High |

### Authentication and Authorization

| ID | Title | Default Severity |
|----|-------|------------------|
| [TG-AUTH-001](TG-AUTH-001-weak-password-storage.md) | Weak Password Storage | Critical |
| [TG-AUTH-002](TG-AUTH-002-client-only-authorization.md) | Client-Only Authorization | High |
| [TG-AUTH-003](TG-AUTH-003-missing-object-authorization.md) | Missing Object-Level Authorization (IDOR) | High |
| [TG-AUTH-004](TG-AUTH-004-insecure-session-cookie.md) | Insecure Session Cookie | High |
| [TG-AUTH-005](TG-AUTH-005-unsafe-password-reset.md) | Unsafe Password Reset or Account Recovery | High |

### Rate Limiting and Resource Abuse

| ID | Title | Default Severity |
|----|-------|------------------|
| [TG-RATE-001](TG-RATE-001-unlimited-auth-endpoint.md) | Unlimited Authentication Endpoint | High |
| [TG-RATE-002](TG-RATE-002-unlimited-public-write-endpoint.md) | Unlimited Public Write or Expensive Endpoint | Medium |
| [TG-RATE-003](TG-RATE-003-unbounded-resource-consumption.md) | Unbounded Resource Consumption | High |

### Client Exposure

| ID | Title | Default Severity |
|----|-------|------------------|
| [TG-CLIENT-001](TG-CLIENT-001-public-production-source-maps.md) | Public Production Source Maps | Medium |
| [TG-CLIENT-002](TG-CLIENT-002-sensitive-client-bundle-content.md) | Sensitive Client Bundle Content | High |

### Platform Hardening

| ID | Title | Default Severity |
|----|-------|------------------|
| [TG-PLATFORM-001](TG-PLATFORM-001-wildcard-cors-with-credentials.md) | Wildcard CORS With Credentials | High |
| [TG-PLATFORM-002](TG-PLATFORM-002-missing-security-headers.md) | Missing Security Headers | Medium |
| [TG-PLATFORM-003](TG-PLATFORM-003-production-stack-trace-exposure.md) | Production Stack Trace or Internal Error Exposure | Medium |
| [TG-PLATFORM-004](TG-PLATFORM-004-missing-request-size-limits.md) | Missing Request Size Limits | Medium |

## Area Mapping for `/TorusGuard check`

| Area | Rules |
|------|-------|
| `secrets` | TG-SEC-001 … TG-SEC-004 |
| `database` | TG-DB-001 … TG-DB-003 |
| `input` | TG-INPUT-001 … TG-INPUT-004 |
| `auth` | TG-AUTH-001 … TG-AUTH-005 |
| `rate-limit` | TG-RATE-001 … TG-RATE-003 |
| `client` | TG-CLIENT-001 … TG-CLIENT-002 |
| `platform` | TG-PLATFORM-001 … TG-PLATFORM-004 |

## Related Documentation

- Reference modules: `skills/TorusGuard/references/`
- Framework guides: `guides/`
- Example mappings: `examples/vulnerable-react-express/vulnerabilities.md`, `examples/hardened-react-express/fixes.md`
