# TG-SSRF-003: Unsafe Redirect Following

## Severity
High. Configuring server-side HTTP clients to automatically follow redirects allows attackers to bypass initial URL allowlists by supplying a public URL that redirects (301/302) to an internal loopback or cloud metadata service.

## Applies To
- HTTP Clients (Axios, Requests, Fetch, urllib, cURL)
- Node.js, Python, Go, Java

## Why It Matters
An application might validate that `https://example.com/image.png` is safe. However, if `example.com` returns a redirect header `Location: http://169.254.169.254/latest/meta-data/` and the client follows redirects automatically, the internal metadata service is fetched.

## What TorusGuard Looks For
- HTTP client configurations with `maxRedirects > 0`, `follow_redirects=True`, or `allow_redirects=True` on user-controlled fetches.

## Unsafe Example
```javascript
// UNSAFE: Axios configured with default automatic redirect following
const response = await axios.get(userSuppliedUrl, { maxRedirects: 5 });
```

## Safe Example
```javascript
// SAFE: Disabling automatic redirect following or revalidating redirect target
const response = await axios.get(userSuppliedUrl, {
  maxRedirects: 0,
  validateStatus: status => status >= 200 && status < 300
});
```

## Ponytail Remediation Budget
- Additions: <= 4 lines
- Deletions: <= 2 lines

## Remediation
1. Disable automatic HTTP redirect following (`maxRedirects: 0` or `allow_redirects=False`).
2. If redirects must be supported, intercept `Location` headers and re-run IP safety checks before dispatching secondary requests.

## Related Rules
- `TG-SSRF-001`: User-Controlled Server-Side URL Fetch
- `TG-SSRF-002`: Missing Internal Network Protection
