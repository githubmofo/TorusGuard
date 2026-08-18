# Fix Mapping — hardened-react-express

| Rule ID | Fix applied |
|---------|-------------|
| TG-SEC-001 | JWT secret from `process.env.JWT_SECRET` |
| TG-SEC-002 | Client `.env.example` has only public `VITE_API_URL` |
| TG-SEC-003 | `.env` in `.gitignore`; `.env.example` with placeholders |
| TG-SEC-004 | Structured logging; passwords/tokens redacted |
| TG-DB-001 | All data access via API; no SQL in client |
| TG-DB-002 | No database URLs in client config |
| TG-DB-003 | No admin/ORM SDK in client |
| TG-INPUT-001 | Zod validation on all mutating routes |
| TG-INPUT-002 | Parameterized-style lookup (no string SQL) |
| TG-INPUT-003 | User bio rendered as text, not raw HTML |
| TG-INPUT-004 | Upload stub with size/type/auth checks documented |
| TG-AUTH-001 | bcrypt password hashing |
| TG-AUTH-002 | Admin route protected server-side |
| TG-AUTH-003 | `/api/users/me` only; ownership on resources |
| TG-AUTH-004 | httpOnly, Secure (prod), SameSite cookies |
| TG-AUTH-005 | Random reset token, neutral response, rate limit |
| TG-RATE-001 | `express-rate-limit` on login and reset |
| TG-RATE-002 | Limits on contact and AI endpoints |
| TG-RATE-003 | JSON body limit, pagination cap on search |
| TG-CLIENT-001 | `sourcemap: false` in Vite production build |
| TG-CLIENT-002 | No token logging in client |
| TG-PLATFORM-001 | CORS allowlist |
| TG-PLATFORM-002 | Helmet security headers |
| TG-PLATFORM-003 | Generic error responses in production |
| TG-PLATFORM-004 | Explicit `express.json({ limit: '100kb' })` |
