# Vulnerability Mapping — vulnerable-react-express

Every intentional flaw maps to a TorusGuard rule ID.

| Rule ID | Location | Issue |
|---------|----------|-------|
| TG-SEC-001 | `server/index.js` | Hardcoded JWT secret |
| TG-SEC-002 | `client/.env.example` | Sensitive value in `VITE_` prefix |
| TG-SEC-003 | Documented in README | `.env` must not be committed (example uses `.env.example` only) |
| TG-SEC-004 | `server/index.js` | Logs password and token on login |
| TG-DB-001 | `client/src/App.jsx` | SQL query string built in frontend |
| TG-DB-002 | `client/src/config.js` | Non-functional placeholder DB URL in client config |
| TG-DB-003 | Comment in `client/src/App.jsx` | Documents forbidden Prisma-in-browser pattern |
| TG-INPUT-001 | `server/index.js` `/api/contact` | No validation schema |
| TG-INPUT-002 | `server/index.js` `/api/search` | SQL concatenation |
| TG-INPUT-003 | `client/src/App.jsx` | `dangerouslySetInnerHTML` with user bio |
| TG-INPUT-004 | `server/index.js` `/api/upload` | No size/type/auth checks |
| TG-AUTH-001 | `server/index.js` | Plaintext password comparison |
| TG-AUTH-002 | `client/src/App.jsx` | Client-only admin panel visibility |
| TG-AUTH-003 | `server/index.js` `/api/users/:id` | IDOR — no ownership check |
| TG-AUTH-004 | `server/index.js` | Cookie missing httpOnly/Secure/SameSite |
| TG-AUTH-005 | `server/index.js` `/api/reset` | Predictable reset token, enumeration |
| TG-RATE-001 | `server/index.js` `/api/login` | No rate limit |
| TG-RATE-002 | `server/index.js` `/api/contact`, `/api/ai` | Unlimited public write/AI |
| TG-RATE-003 | `server/index.js` | No body limit, unbounded search results |
| TG-CLIENT-001 | `client/vite.config.js` | `sourcemap: true` |
| TG-CLIENT-002 | `client/src/App.jsx` | `console.log` with token |
| TG-PLATFORM-001 | `server/index.js` | CORS `*` with credentials |
| TG-PLATFORM-002 | `server/index.js` | No Helmet/security headers |
| TG-PLATFORM-003 | `server/index.js` | Returns `err.stack` to client |
| TG-PLATFORM-004 | `server/index.js` | No JSON body size limit |

## Audit exercise

Run `/TorusGuard audit` against this folder and verify your agent finds each rule with file evidence.
