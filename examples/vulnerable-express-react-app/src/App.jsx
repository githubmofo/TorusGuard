import { useState } from 'react';

// TORUSGUARD-DEMO: SQL in frontend — frontend-no-db module
async function searchUsersInBrowser(email) {
  const dbUrl = 'http://localhost:3001/api/raw-search';
  const query = `SELECT * FROM users WHERE email LIKE '%${email}%'`;
  console.log('Running query:', query);
  const res = await fetch(`${dbUrl}?q=${encodeURIComponent(email)}`);
  return res.json();
}

export default function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [search, setSearch] = useState('');
  const [results, setResults] = useState(null);
  const [userId, setUserId] = useState('1');
  const [profile, setProfile] = useState(null);
  const [message, setMessage] = useState('');

  async function handleLogin(e) {
    e.preventDefault();
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    // TORUSGUARD-DEMO: console.log exposes token — client-code-exposure
    console.log('Login response:', data);
    setMessage(data.message || data.error || JSON.stringify(data));
  }

  async function handleSearch() {
    const data = await searchUsersInBrowser(search);
    setResults(data);
  }

  async function fetchProfile() {
    const res = await fetch(`/api/users/${userId}`);
    const data = await res.json();
    setProfile(data);
  }

  return (
    <div style={{ fontFamily: 'sans-serif', maxWidth: 600, margin: '2rem auto' }}>
      <h1>Vulnerable Demo App</h1>
      <p style={{ color: 'crimson' }}>Intentionally insecure — for TorusGuard demos only</p>

      <section>
        <h2>Login</h2>
        <form onSubmit={handleLogin}>
          <input placeholder="email" value={email} onChange={(e) => setEmail(e.target.value)} />
          <input placeholder="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          <button type="submit">Login</button>
        </form>
        {message && <pre>{message}</pre>}
      </section>

      <section>
        <h2>Search (frontend SQL demo)</h2>
        <input placeholder="search email" value={search} onChange={(e) => setSearch(e.target.value)} />
        <button onClick={handleSearch}>Search</button>
        {results && <pre>{JSON.stringify(results, null, 2)}</pre>}
      </section>

      <section>
        <h2>User Profile (IDOR demo)</h2>
        <input placeholder="user id" value={userId} onChange={(e) => setUserId(e.target.value)} />
        <button onClick={fetchProfile}>Fetch Profile</button>
        {profile && <pre>{JSON.stringify(profile, null, 2)}</pre>}
      </section>
    </div>
  );
}
