# Hardened React + Express Example

Secure counterpart to [vulnerable-react-express](../vulnerable-react-express/). Demonstrates TorusGuard remediation patterns.

See [fixes.md](fixes.md) for rule-by-rule mapping.

## Limitations

- Minimal demo for documentation — not a production starter template
- Uses in-memory user store and fake env placeholders
- Rate limiting uses in-memory store (use Redis in distributed production)

## Local setup

```bash
cp server/.env.example server/.env
# Set JWT_SECRET to a long random string
cd server && npm install && npm start
cd client && npm install && npm run dev
```

Demo password for seeded users: `DemoPass123!`

## Structure

```
hardened-react-express/
├── client/    # React + Vite
├── server/    # Express with Zod, bcrypt, Helmet, rate limits
├── fixes.md
└── README.md
```
