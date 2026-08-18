// TG-DB-002: Non-functional placeholder — simulates credential in browser config
export const clientConfig = {
  apiUrl: import.meta.env.VITE_API_URL,
  // FAKE DEMO ONLY — never put real database URLs in client code
  demoDbUrl: 'postgresql://demo:FAKE_PASSWORD@localhost:5432/demo',
};
