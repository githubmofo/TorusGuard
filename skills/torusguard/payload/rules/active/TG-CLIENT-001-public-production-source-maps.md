# TG-CLIENT-001: Public Production Source Maps

## Severity

Medium

## Applies To

- Vite production builds (`build.sourcemap`)
- Next.js production source map settings (`productionBrowserSourceMaps`)
- Create React App/Webpack production `devtool` configuration
- Static hosting/CDN configurations that publish `.map` assets publicly
- Any SPA/SSR frontend bundle served to untrusted clients

## Why It Matters

Source maps improve debugging, but can expose internal implementation details.
Public `.map` files make reverse engineering easier at scale.
Attackers can quickly recover original symbols, comments, and code structure.
This increases the efficiency of finding hidden routes, feature flags, and weak points.
It does not create a vulnerability alone, but it lowers attacker effort materially.
Browser DevTools cannot be blocked, so exposure must be reduced at build and hosting layers.

## What TorusGuard Looks For

- Build configs enabling source maps for production bundles
- Presence of emitted `*.js.map` or `*.css.map` in deploy artifacts
- CDN/static host rules that allow unauthenticated access to map files
- Missing split behavior (private error telemetry maps vs public maps)
- Framework defaults overridden to expose maps in production
- CI pipelines that upload maps to public artifact locations

## Unsafe Example

```ts
// vite.config.ts
import { defineConfig } from "vite";

export default defineConfig({
  build: {
    sourcemap: true
  }
});
```

```js
// next.config.js
module.exports = {
  productionBrowserSourceMaps: true
};
```

## Safe Example

```ts
// vite.config.ts
import { defineConfig } from "vite";

export default defineConfig({
  build: {
    sourcemap: false
  }
});
```

```js
// next.config.js
module.exports = {
  productionBrowserSourceMaps: false
};
```

## Remediation

1. Disable public production source maps by default in Vite/Next/CRA/Webpack.
2. If stack-trace symbolication is required, upload maps to a private error-monitoring service only.
3. Block direct `.map` retrieval on CDN and static hosting layers.
4. Validate build pipelines do not copy maps into public deployment folders.
5. Remove already published map files from current and prior versions where feasible.
6. Document an exception process for temporary debugging in production.
7. Pair with bundle scanning to ensure sensitive literals are not shipped regardless.

## Verification

- Build production artifacts and confirm no `*.map` files in public output.
- Request known map paths in deployed environments and verify denial/404 behavior.
- Check framework configs (`vite.config`, `next.config`, webpack overrides) for safe values.
- Confirm telemetry symbolication still works via private upload channels where used.
- Validate rollback artifacts are also map-free in release storage.

## False Positives and Exceptions

- Private internal tools served only behind corporate SSO and network controls
- Short-lived troubleshooting releases with approved exception and explicit expiry
- Source maps uploaded privately to monitoring vendor, not served publicly
- Bundles where maps exist on disk but are never deployed to public hosts

## Related Rules

- `TG-CLIENT-002-sensitive-client-bundle-content.md`
- `TG-PLATFORM-003-production-stack-trace-exposure.md`
- `TG-SEC-002-public-environment-secrets.md`
