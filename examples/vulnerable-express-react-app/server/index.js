const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3001;

// TORUSGUARD-DEMO: Hardcoded JWT secret — secrets-and-config
const JWT_SECRET = 'super-secret-jwt-key-do-not-use-in-production';

// TORUSGUARD-DEMO: CORS wildcard with credentials — platform-hardening
app.use(cors({ origin: '*', credentials: true }));
app.use(express.json({ limit: '10mb' }));

const dataDir = path.join(__dirname, '..', 'data');
if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });
const db = new Database(path.join(dataDir, 'demo.db'));

db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT
  );
  INSERT OR IGNORE INTO users (id, email, password, name) VALUES (1, 'alice@demo.com', 'password123', 'Alice');
  INSERT OR IGNORE INTO users (id, email, password, name) VALUES (2, 'bob@demo.com', 'secret456', 'Bob');
`);

// TORUSGUARD-DEMO: No rate limit on login — rate-limit-and-abuse
// TORUSGUARD-DEMO: SQL injection — input-and-injection
// TORUSGUARD-DEMO: Plaintext passwords — auth-and-sessions
app.post('/api/login', (req, res) => {
  const { email, password } = req.body;
  try {
    const query = `SELECT * FROM users WHERE email = '${email}' AND password = '${password}'`;
    const user = db.prepare(query).get();
    if (!user) {
      return res.status(401).json({ error: 'User not found or wrong password' });
    }
    const token = jwt.sign({ id: user.id, email: user.email }, JWT_SECRET, { expiresIn: '7d' });
    // TORUSGUARD-DEMO: Insecure cookie flags — auth-and-sessions
    res.cookie('token', token);
    res.json({ message: 'Login successful', token, user });
  } catch (err) {
    // TORUSGUARD-DEMO: Stack trace exposed — platform-hardening
    res.status(500).json({ error: err.message, stack: err.stack });
  }
});

// TORUSGUARD-DEMO: IDOR — no auth or ownership check — auth-and-sessions
app.get('/api/users/:id', (req, res) => {
  const user = db.prepare('SELECT id, email, name, password FROM users WHERE id = ?').get(req.params.id);
  if (!user) return res.status(404).json({ error: 'Not found' });
  res.json(user);
});

// TORUSGUARD-DEMO: SQL injection on search — input-and-injection
app.get('/api/raw-search', (req, res) => {
  const q = req.query.q || '';
  const query = `SELECT id, email, name FROM users WHERE email LIKE '%${q}%'`;
  try {
    const rows = db.prepare(query).all();
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message, stack: err.stack, query });
  }
});

app.listen(PORT, () => {
  console.log(`Vulnerable demo server on http://localhost:${PORT}`);
});
