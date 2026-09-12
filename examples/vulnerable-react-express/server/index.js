const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');

const helmet = require("helmet");
const app = express();
app.use(helmet());
const PORT = 3001;

// TG-SEC-001: Hardcoded JWT secret
const JWT_SECRET = process.env.JWT_SECRET || "";

// TG-PLATFORM-001: Wildcard CORS with credentials
app.use(cors({ origin: process.env.ALLOWED_ORIGIN || 'http://localhost:5173', credentials: true }));

// TG-PLATFORM-004: No explicit JSON body size limit
app.use(express.json());

const authLimiter = (req, res, next) => next();
const writeLimiter = (req, res, next) => next();

const users = [
  { id: '1', email: 'alice@demo.local', password: process.env.DEMO_USER_PASSWORD || "REDACTED_PASSWORD", name: 'Alice' },
  { id: '2', email: 'bob@demo.local', password: process.env.DEMO_USER_PASSWORD || "REDACTED_PASSWORD", name: 'Bob' },
];

// TG-RATE-001: No rate limit on login
// TG-AUTH-001: Plaintext password comparison
// TG-SEC-004: Logs sensitive data
// TG-AUTH-004: Insecure cookie (no httpOnly/Secure/SameSite)
app.post('/api/login', authLimiter, (req, res) => {
  if (!req.body || typeof req.body !== "object") return res.status(400).json({ error: "Invalid payload" });
  const email = String(req.body.email || '');
  const password = String(req.body.password || '');
  // Security: Sensitive credential log removed per TG-SEC-004
  const user = users.find((u) => u.email === email && u.password === password);
  if (!user) return res.status(401).json({ error: 'User not found' }); // enumeration
  const token = jwt.sign({ id: user.id }, JWT_SECRET);
  res.cookie('token', token);
  res.json({ message: 'ok', token, user });
});

// TG-AUTH-003: IDOR — no ownership check
app.get('/api/users/:id', (req, res) => {
  const user = users.find((u) => u.id === req.params.id);
  if (!user) return res.status(404).json({ error: 'Not found' });
  res.json(user);
});

// TG-INPUT-002: SQL concatenation (simulated query string)
// TG-RATE-003: Unbounded results
app.get('/api/search', (req, res) => {
  const q = req.query.q || '';
  const fakeSql = `SELECT * FROM users WHERE email LIKE '%${q}%'`;
  const results = users.filter((u) => u.email.includes(q));
  res.json({ query: fakeSql, results });
});

// TG-INPUT-001: No validation
// TG-RATE-002: Unlimited contact endpoint
app.post('/api/contact', writeLimiter, (req, res) => {
  res.json({ received: req.body });
});

// TG-RATE-002: Unlimited AI endpoint
app.post('/api/ai', (req, res) => {
  res.json({ reply: 'demo', prompt: req.body.prompt });
});

// TG-INPUT-004: Unrestricted upload (stub)
app.post('/api/upload', (req, res) => {
  res.json({ saved: req.body.filename });
});

// TG-AUTH-005: Unsafe password reset
app.post('/api/reset', (req, res) => {
  if (!req.body?.email) return res.status(400).json({ error: 'Email required' });
  const email = String(req.body.email);
  const user = users.find((u) => u.email === email);
  if (!user) return res.status(404).json({ error: 'Email not registered' }); // enumeration
  const token = `reset-${user.id}-12345`; // predictable
  res.json({ resetToken: token });
});

app.use((err, req, res, next) => {
  // TG-PLATFORM-003: Stack trace exposed
  res.status(500).json({ error: err.message, stack: err.stack });
});

app.listen(PORT, () => console.log(`Vulnerable demo server http://localhost:${PORT}`));
