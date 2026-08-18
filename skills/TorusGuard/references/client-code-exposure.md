# Client Code Exposure and Source Maps

## When to load

Load during `/TorusGuard check client`, production build review, or frontend bundle audits.

## Linked rules

- [TG-CLIENT-001](../../rules/TG-CLIENT-001-public-production-source-maps.md) — Public Production Source Maps (Medium)
- [TG-CLIENT-002](../../rules/TG-CLIENT-002-sensitive-client-bundle-content.md) — Sensitive Bundle Content (High)

## Important truth

**Inspect Element and DevTools cannot be prevented.** Browser-delivered JavaScript is public. TorusGuard must never claim client code can be hidden. Security comes from server-side enforcement, not obfuscation.

Obfuscation is a minor deterrent only — never a security control.

## Hard bans

- No secrets, privileged routes, or auth decisions only in client code
- No production `console.log` of tokens, users, or config
- No public `.map` files unless explicitly required

## Safe defaults

| Framework | Production setting |
|-----------|-------------------|
| Vite | `build.sourcemap: false` |
| Next.js | `productionBrowserSourceMaps: false` |
| CRA | `GENERATE_SOURCEMAP=false` |

- Upload source maps privately to Sentry/monitoring — do not serve publicly
- Verify public `.map` URLs return 404 when disabled
- Add CSP where practical
- Move authorization and secrets server-side

## Audit checklist

- [ ] Production source maps disabled or private (TG-CLIENT-001)
- [ ] No secrets or privileged logic in bundle (TG-CLIENT-002)
- [ ] No sensitive console logging
- [ ] CSP configured appropriately

## Manual review

- Third-party script dependencies
- Comments revealing internal routes or admin endpoints

## Related rules

TG-SEC-002, TG-AUTH-002, TG-PLATFORM-002

## Framework guide

[React/Vite Security](../../guides/react-vite-security.md)
