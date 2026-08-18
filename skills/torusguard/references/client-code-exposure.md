# Client Code Exposure and Source Maps

## Scope

Reduce unnecessary exposure of original source files, comments, route hints, API details, and secrets through production builds.

## Important Truth

**DevTools cannot be blocked.** Browser-delivered JavaScript is public. Security comes from server-side enforcement, not from hiding client code.

TorusGuard must never claim that Inspect Element, DevTools, or browser Sources can be blocked.

## Threat Model

- Public source maps reveal original TypeScript/React source
- Comments expose internal routes, admin endpoints, or credentials
- `console.log` leaks tokens and user objects in production
- Sensitive business rules or admin logic in browser bundles
- Missing CSP allows XSS exploitation

## Detection Patterns

| Pattern | Severity |
|---------|----------|
| Vite `build.sourcemap: true` in production config | High |
| Next.js `productionBrowserSourceMaps: true` | High |
| `.map` files in `dist/` or `build/` deployed publicly | High |
| `console.log` with tokens, users, or config in production code | Medium |
| Admin/role logic only in frontend components | Critical |
| Secrets in frontend bundle (via env or hardcode) | Critical |
| Missing Content-Security-Policy | Medium |

## Required Fixes

### Vite

```javascript
// vite.config.js
export default defineConfig({
  build: {
    sourcemap: false,
  },
});
```

### Next.js

```javascript
// next.config.js
const nextConfig = {
  productionBrowserSourceMaps: false,
};
export default nextConfig;
```

### Create React App

```env
GENERATE_SOURCEMAP=false
```

### Additional requirements

- Do not deploy public `.map` files unless explicitly required
- If Sentry or monitoring requires maps, upload privately — do not serve publicly
- CDN/deployment should return 404 for public `.map` files when disabled
- Strip development logs in production builds where appropriate
- Keep secrets and authorization logic server-side
- Add CSP where practical

### Content-Security-Policy example

```javascript
app.use((req, res, next) => {
  res.setHeader(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self' https://api.example.com"
  );
  next();
});
```

## Hard Bans

- No secret in browser-delivered code
- No client-only authorization decision protecting sensitive data
- No production logs exposing authentication material

## Verification Checklist

- [ ] Production source maps not publicly accessible (unless intentional)
- [ ] No secret in browser bundle
- [ ] No client-only authorization for sensitive data
- [ ] Production builds strip or disable debug logging
- [ ] CSP configured where practical

## False-Positive Guidance

- Source maps enabled in **development** only — expected
- Private source map upload to Sentry during CI — OK if not publicly served
- Minified variable names still expose logic — focus on secrets and auth, not obfuscation

## Remediation Steps

1. Disable public production source maps
2. Remove secrets and privileged logic from frontend
3. Move authorization to server
4. Add CSP headers
5. Remove or guard production console.log statements
