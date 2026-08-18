# Input Validation and Injection Prevention

## Scope

Treat all external input as untrusted and validate it at the server boundary.

## Threat Model

- SQL/NoSQL injection via concatenated queries
- XSS via unsanitized HTML rendering
- Command injection via shell execution
- Open redirects via user-controlled URLs
- Malicious file uploads

## Untrusted Input Sources

- Request body, query params, path params, headers, cookies
- Form submissions, webhooks, file uploads
- Imported CSV/Excel/JSON files
- Third-party API responses, LLM responses
- Database values later rendered as HTML

## Detection Patterns

| Pattern | Severity |
|---------|----------|
| SQL string concatenation with `req.body`, `req.query`, `req.params` | Critical |
| `eval()`, `new Function()`, `child_process.exec` with user input | Critical |
| `dangerouslySetInnerHTML` without sanitization | High |
| Missing validation before business logic in API routes | High |
| Redirect: `res.redirect(req.query.url)` without allowlist | High |
| File upload accepted by extension only | Medium |
| Trust in `req.body.role`, `req.body.isAdmin`, `req.body.userId` | Critical |

## Hard Bans

- No raw string-concatenated SQL
- No `eval`, `Function()`, or dynamic code execution with untrusted input
- No direct shell execution with user input
- No unsanitized user-generated HTML rendering
- No user-controlled redirect without an allowlist
- No file upload accepted only by filename extension
- No trust in `req.body.role`, `isAdmin`, or `userId`

## Required Safe Defaults

### Schema validation (Zod example)

```javascript
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email().max(255),
  password: z.string().min(8).max(128),
});

router.post('/login', async (req, res) => {
  const parsed = loginSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ error: 'Invalid input' });
  }
  const { email, password } = parsed.data;
  // business logic
});
```

### Parameterized queries

```javascript
// Safe
await db.query('SELECT * FROM users WHERE email = $1', [email]);

// Unsafe — NEVER
await db.query(`SELECT * FROM users WHERE email = '${email}'`);
```

### File uploads

```javascript
const upload = multer({
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB
  fileFilter: (req, file, cb) => {
    const allowed = ['image/jpeg', 'image/png', 'application/pdf'];
    if (!allowed.includes(file.mimetype)) {
      return cb(new Error('Invalid file type'));
    }
    cb(null, true);
  },
});
// Store outside web root; generate server-side filename
```

### Redirect allowlist

```javascript
const ALLOWED_REDIRECTS = ['/dashboard', '/settings', '/'];

function safeRedirect(url) {
  if (!url.startsWith('/') || url.startsWith('//')) return '/';
  return ALLOWED_REDIRECTS.includes(url) ? url : '/';
}
```

## Framework-Specific Examples

| Stack | Validation approach |
|-------|---------------------|
| Express | Zod/Joi middleware before route handler |
| Next.js API routes | Zod parse in route handler or middleware |
| Next.js Server Actions | Validate with Zod at action entry |
| Supabase | RLS + Edge Function validation for mutations |

## Verification Checklist

- [ ] Every API route validates request input
- [ ] Every database query uses parameters or safe ORM
- [ ] File upload routes have size, type, and authorization checks
- [ ] HTML rendering of untrusted content is sanitized or avoided
- [ ] Redirect URLs use allowlist
- [ ] No shell/command execution with user input

## False-Positive Guidance

- ORM methods like `prisma.user.findMany({ where: { id } })` — parameterized by ORM, not injection
- Validated enums after Zod parse — safe
- Server-side template rendering with auto-escaped engines (EJS default) — lower risk

## Remediation Steps

1. Add schema validation at route entry
2. Replace concatenated SQL with parameterized queries
3. Add upload restrictions and server-side filenames
4. Sanitize HTML only when rich HTML is genuinely required (use DOMPurify)
