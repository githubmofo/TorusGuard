# Vulnerable React + Express Example

**WARNING: This application is intentionally vulnerable. Do not deploy it, expose it to the internet, or reuse its security patterns.**

Documentation-only reference for TorusGuard v0.2.0. See [vulnerabilities.md](vulnerabilities.md) for the full rule mapping.

## Structure

```
vulnerable-react-express/
├── client/          # React + Vite (browser code)
├── server/          # Express API
├── vulnerabilities.md
└── README.md
```

## Local setup (isolated lab only)

```bash
cd examples/vulnerable-react-express/server && npm install && npm start
cd examples/vulnerable-react-express/client && npm install && npm run dev
```

Run only on localhost. Do not bind to `0.0.0.0` or deploy.

## What this demonstrates

22 intentional violations across all TorusGuard rule categories. Each marked with `// TG-RULE-ID` comments in source.

## Safe alternative

See [../hardened-react-express/](../hardened-react-express/).
