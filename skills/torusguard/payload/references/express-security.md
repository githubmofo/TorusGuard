# Express Security Guide

## When to use

Load during audits of Node.js Express APIs serving web or mobile clients.

**Related rules:** TG-INPUT-001, TG-INPUT-002, TG-AUTH-003, TG-AUTH-004, TG-RATE-001, TG-PLATFORM-001 … TG-PLATFORM-004

## Checklist

- [ ] Helmet or equivalent security headers (TG-PLATFORM-002)
- [ ] CORS explicit allowlist — never `*` with credentials (TG-PLATFORM-001)
- [ ] `express.json({ limit: '100kb' })` or appropriate cap (TG-PLATFORM-004)
- [ ] Zod/Joi validation on every mutating route (TG-INPUT-001)
- [ ] Parameterized SQL or ORM — no concatenation (TG-INPUT-002)
- [ ] Rate limits on login, reset, OTP (TG-RATE-001)
- [ ] Central error handler — generic client messages (TG-PLATFORM-003)
- [ ] Secure cookie flags for sessions (TG-AUTH-004)
- [ ] Ownership middleware on resource routes (TG-AUTH-003)

## Baseline server setup

```javascript
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import rateLimit from 'express-rate-limit';

const app = express();
const allowedOrigins = ['https://app.example.com'];

app.use(helmet());
app.use(cors({
  origin(origin, cb) {
    if (!origin || allowedOrigins.includes(origin)) cb(null, true);
    else cb(new Error('Not allowed by CORS'));
  },
  credentials: true,
}));
app.use(express.json({ limit: '100kb' }));

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  standardHeaders: true,
  message: { error: 'Too many attempts' },
});
app.post('/api/login', loginLimiter, loginHandler);
```

## Validation middleware

```javascript
import { z } from 'zod';

function validate(schema) {
  return (req, res, next) => {
    const parsed = schema.safeParse({ body: req.body, query: req.query, params: req.params });
    if (!parsed.success) return res.status(400).json({ error: 'Invalid input' });
    req.validated = parsed.data;
    next();
  };
}
```

## Ownership middleware

```javascript
async function requireOrderOwner(req, res, next) {
  const order = await db.order.findUnique({ where: { id: req.params.id } });
  if (!order || order.userId !== req.user.id) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  req.order = order;
  next();
}
```

## Error handler

```javascript
app.use((err, req, res, next) => {
  console.error({ err, requestId: req.id });
  res.status(err.status || 500).json({
    error: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message,
  });
});
```

## Distributed rate limiting

Use Redis or similar shared store in multi-instance production — in-memory limiters alone are insufficient (TG-RATE-001).

## Manual review

- Enumerate all `app.use` order (auth before routes)
- Verify upload routes have size/type/auth checks
- Run dependency audit before deploy

## Related documentation

- [rules/TG-PLATFORM-001-wildcard-cors-with-credentials.md](../rules/TG-PLATFORM-001-wildcard-cors-with-credentials.md)
- [skills/TorusGuard/references/platform-hardening.md](../skills/TorusGuard/references/platform-hardening.md)
