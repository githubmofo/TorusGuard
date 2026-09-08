# TG-SSRF-001: User-Controlled Server-Side URL Fetch

## Severity
High by default. Raise to Critical when the request can reach internal administrative services, cloud metadata services, or sensitive network assets.

## Applies To
- URL preview APIs
- Remote image/file importers
- Webhook testers
- PDF generation services
- Server-side integrations
- Any endpoint that fetches a URL supplied by a user

## Why It Matters
A server that fetches an attacker-controlled URL may be used to access internal systems or send requests from a trusted network location.

## What TorusGuard Looks For
- fetch(), axios, requests, HttpClient, OkHttp, or equivalent calls
- URL values derived from request body, query, or path parameters
- Redirect-following enabled without destination validation
- No domain or IP allowlist
- No timeout or response-size limit

## Unsafe Example
```javascript
const response = await fetch(req.body.url);
```

## Safe Example
```javascript
const target = new URL(req.body.url);
if (target.protocol !== "https:") {
  throw new Error("Only HTTPS URLs are allowed");
}
if (!ALLOWED_HOSTS.has(target.hostname)) {
  throw new Error("Destination is not allowed");
}
const response = await fetch(target, {
  redirect: "error",
  signal: AbortSignal.timeout(5000)
});
```

## Remediation
1. Parse the URL using a maintained URL parser.
2. Allow only required schemes.
3. Prefer an explicit hostname allowlist.
4. Block private, loopback, link-local, and metadata destinations.
5. Disable or revalidate redirects.
6. Apply timeout and response-size limits.
7. Do not return raw upstream responses.

## Verification
- Test allowed domains.
- Test localhost and loopback addresses.
- Test private IP ranges.
- Test metadata-service addresses.
- Test file:// and other unsupported schemes.
- Test redirects to an untrusted or internal destination.
- Verify timeout and response-size behavior.

## False Positives and Exceptions
An exception requires a documented fixed allowlist, network isolation, timeout, response limit, and review owner.

## Related Rules
- TG-SSRF-002
- TG-SSRF-003
- TG-RATE-003
