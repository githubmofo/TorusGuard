# Hardened TorusGuard Demo App

Secure counterpart to `examples/vulnerable-express-react-app/`.

## Security fixes applied

| Module | Fix |
|--------|-----|
| secrets-and-config | JWT secret from env; `.env.example` with placeholders |
| frontend-no-db | All DB access through API; no SQL in frontend |
| input-and-injection | Zod validation; parameterized queries |
| auth-and-sessions | bcrypt passwords; httpOnly cookies; ownership checks |
| rate-limit-and-abuse | Rate limit on login; body size limits |
| client-code-exposure | Source maps disabled; no token logging |
| platform-hardening | Helmet; CORS allowlist; sanitized errors |

## Setup

```bash
cp .env.example .env
# Edit .env and set JWT_SECRET to a long random string
npm install
npm run dev
```

Server: http://localhost:3001  
Client: http://localhost:5173

Demo users (password: `demo1234`):
- alice@demo.com
- bob@demo.com
