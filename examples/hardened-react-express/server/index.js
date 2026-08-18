require('dotenv').config();
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const cookieParser = require('cookie-parser');
const rateLimit = require('express-rate-limit');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const { z } = require('zod');

if (!process.env.JWT_SECRET) {
  console.error('Missing JWT_SECRET');
  process.exit(1);
}

const app = express();
const PORT = 3001;
const isProd = process.env.NODE_ENV === 'production';

app.use(helmet());
app.use(cors({ origin: process.env.CLIENT_ORIGIN, credentials: true }));
app.use(express.json({ limit: '100kb' }));
app.use(cookieParser());

const loginLimiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 5 });
const resetLimiter = rateLimit({ windowMs: 60 * 60 * 1000, max: 3 });
const publicWriteLimiter = rateLimit({ windowMs: 60 * 60 * 1000, max: 10 });

const users = [];
const resetTokens = new Map();

async function seed() {
  if (users.length) return;
  const hash = await bcrypt.hash('DemoPass123!', 12);
  users.push({ id: '1', email: 'alice@demo.local', passwordHash: hash, name: 'Alice', role: 'user' });
  users.push({ id: '2', email: 'bob@demo.local', passwordHash: hash, name: 'Bob', role: 'user' });
}

const loginSchema = z.object({
  email: z.string().email().max(255),
  password: z.string().min(8).max(128),
});

function auth(req, res, next) {
  const token = req.cookies.token;
  if (!token) return res.status(401).json({ error: 'Unauthorized' });
  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    next();
  } catch {
    return res.status(401).json({ error: 'Unauthorized' });
  }
}

app.post('/api/login', loginLimiter, async (req, res) => {
  const parsed = loginSchema.safeParse(req.body);
  if (!parsed.success) return res.status(400).json({ error: 'Invalid input' });
  const { email, password } = parsed.data;
  const user = users.find((u) => u.email === email);
  if (!user || !(await bcrypt.compare(password, user.passwordHash))) {
    return res.status(401).json({ error: 'Invalid email or password' });
  }
  const token = jwt.sign({ id: user.id, role: user.role }, process.env.JWT_SECRET, { expiresIn: '1h' });
  res.cookie('token', token, {
    httpOnly: true,
    secure: isProd,
    sameSite: 'lax',
    maxAge: 3600000,
  });
  res.json({ message: 'Login successful' });
});

app.get('/api/users/me', auth, (req, res) => {
  const user = users.find((u) => u.id === req.user.id);
  if (!user) return res.status(404).json({ error: 'Not found' });
  res.json({ id: user.id, email: user.email, name: user.name });
});

app.get('/api/search', auth, (req, res) => {
  const q = String(req.query.q || '').slice(0, 100);
  const results = users
    .filter((u) => u.email.includes(q))
    .slice(0, 20)
    .map(({ id, email, name }) => ({ id, email, name }));
  res.json({ results });
});

const contactSchema = z.object({ message: z.string().min(1).max(2000) });
app.post('/api/contact', publicWriteLimiter, (req, res) => {
  const parsed = contactSchema.safeParse(req.body);
  if (!parsed.success) return res.status(400).json({ error: 'Invalid input' });
  res.json({ ok: true });
});

app.post('/api/ai', auth, publicWriteLimiter, (req, res) => {
  const prompt = String(req.body.prompt || '').slice(0, 4000);
  res.json({ reply: 'demo response', length: prompt.length });
});

app.post('/api/reset', resetLimiter, (req, res) => {
  const email = String(req.body.email || '');
  const user = users.find((u) => u.email === email);
  if (user) {
    const token = crypto.randomBytes(32).toString('hex');
    resetTokens.set(token, { userId: user.id, expires: Date.now() + 900000 });
  }
  res.json({ message: 'If an account exists, a reset link was sent.' });
});

app.get('/api/admin/stats', auth, (req, res) => {
  if (req.user.role !== 'admin') return res.status(403).json({ error: 'Forbidden' });
  res.json({ users: users.length });
});

app.use((err, req, res, next) => {
  console.error('Error', { message: err.message });
  res.status(500).json({ error: isProd ? 'Internal server error' : err.message });
});

seed().then(() => app.listen(PORT, () => console.log(`Hardened demo http://localhost:${PORT}`)));
