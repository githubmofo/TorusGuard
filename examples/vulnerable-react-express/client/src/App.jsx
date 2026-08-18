import { useState } from 'react';
import { clientConfig } from './config';

// TG-DB-001: SQL query construction in frontend (never do this)
function buildSearchQuery(email) {
  return `SELECT id, email FROM users WHERE email LIKE '%${email}%'`;
}

// TG-DB-003: Documented anti-pattern — Prisma must never run in browser
// import { PrismaClient } from '@prisma/client'; // FORBIDDEN in client

export default function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [bio, setBio] = useState('<img src=x onerror=alert(1)>');
  const [userId, setUserId] = useState('1');
  const [isAdmin] = useState(localStorage.getItem('role') === 'admin'); // TG-AUTH-002
  const [message, setMessage] = useState('');

  async function login(e) {
    e.preventDefault();
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    // TG-CLIENT-002: Sensitive console logging
    console.log('Login token:', data.token, 'config:', clientConfig);
    setMessage(JSON.stringify(data));
  }

  async function fetchUser() {
    const res = await fetch(`/api/users/${userId}`);
    setMessage(await res.text());
  }

  return (
    <div style={{ maxWidth: 560, margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h1>Vulnerable Demo</h1>
      <p style={{ color: 'crimson' }}>Intentionally insecure — localhost lab only</p>

      <form onSubmit={login}>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="email" />
        <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="password" type="password" />
        <button type="submit">Login</button>
      </form>

      <p>Frontend SQL preview: {buildSearchQuery(email)}</p>

      {/* TG-INPUT-003: Unsafe HTML rendering */}
      <div dangerouslySetInnerHTML={{ __html: bio }} />

      <button onClick={fetchUser}>Fetch user (IDOR demo)</button>

      {/* TG-AUTH-002: Client-only admin gate */}
      {isAdmin && <section><h2>Admin Panel</h2><p>Visible if localStorage role=admin — not real security</p></section>}

      {message && <pre>{message}</pre>}
    </div>
  );
}
