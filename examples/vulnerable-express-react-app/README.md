# INTENTIONALLY INSECURE — DO NOT DEPLOY

This demo app contains deliberate vulnerabilities for TorusGuard training and testing.

## Vulnerabilities (by module)

| Module | Vulnerability |
|--------|---------------|
| secrets-and-config | Hardcoded JWT secret, `.env` with real-looking values |
| frontend-no-db | SQL query in React component |
| input-and-injection | SQL injection on login and search |
| auth-and-sessions | IDOR on `/api/users/:id`, weak cookies |
| rate-limit-and-abuse | No rate limit on login |
| client-code-exposure | Source maps enabled, console.log tokens |
| platform-hardening | CORS wildcard with credentials, stack traces in errors |

## Run locally

```bash
npm install
npm run dev
```

Server: http://localhost:3001  
Client: http://localhost:5173

Compare with `examples/hardened-express-react-app/`.
