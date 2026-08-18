import { useState } from 'react';

export default function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [bio, setBio] = useState('Hello world');
  const [profile, setProfile] = useState(null);
  const [message, setMessage] = useState('');

  async function login(e) {
    e.preventDefault();
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email, password }),
    });
    setMessage((await res.json()).message || 'Login failed');
  }

  async function loadProfile() {
    const res = await fetch('/api/users/me', { credentials: 'include' });
    if (res.ok) setProfile(await res.json());
    else setProfile({ error: 'Unauthorized' });
  }

  return (
    <div style={{ maxWidth: 560, margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h1>Hardened Demo</h1>
      <p style={{ color: 'green' }}>TorusGuard secure patterns</p>
      <form onSubmit={login}>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="email" />
        <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="password" type="password" />
        <button type="submit">Login</button>
      </form>
      <button onClick={loadProfile}>My Profile</button>
      <p>{bio}</p>
      {profile && <pre>{JSON.stringify(profile, null, 2)}</pre>}
      {message && <p>{message}</p>}
    </div>
  );
}
