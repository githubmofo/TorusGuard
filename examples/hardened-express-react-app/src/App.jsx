import { useState } from 'react';

export default function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [search, setSearch] = useState('');
  const [results, setResults] = useState(null);
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
    setMessage(data.message || data.error || 'Login complete');
  }

  async function handleSearch() {
    const res = await fetch(`/api/search?q=${encodeURIComponent(search)}`, {
      credentials: 'include',
    });
    if (!res.ok) {
      setResults({ error: 'Search failed' });
      return;
    }
    setResults(await res.json());
  }

  async function fetchMyProfile() {
    const res = await fetch('/api/users/me', { credentials: 'include' });
    if (!res.ok) {
      setProfile({ error: 'Unauthorized' });
      return;
    }
    setProfile(await res.json());
  }

  return (
    <div style={{ fontFamily: 'sans-serif', maxWidth: 600, margin: '2rem auto' }}>
      <h1>Hardened Demo App</h1>
      <p style={{ color: 'green' }}>TorusGuard hardened example</p>

      <section>
        <h2>Login</h2>
        <form onSubmit={handleLogin}>
          <input placeholder="email" value={email} onChange={(e) => setEmail(e.target.value)} />
          <input placeholder="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          <button type="submit">Login</button>
        </form>
        {message && <p>{message}</p>}
      </section>

      <section>
        <h2>Search (authenticated API)</h2>
        <input placeholder="search email" value={search} onChange={(e) => setSearch(e.target.value)} />
        <button onClick={handleSearch}>Search</button>
        {results && <pre>{JSON.stringify(results, null, 2)}</pre>}
      </section>

      <section>
        <h2>My Profile</h2>
        <button onClick={fetchMyProfile}>Fetch My Profile</button>
        {profile && <pre>{JSON.stringify(profile, null, 2)}</pre>}
      </section>
    </div>
  );
}
