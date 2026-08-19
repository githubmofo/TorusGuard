# SSRF and Outbound Requests

## When the reference applies
Applies to any endpoint that fetches a URL.

## User-controlled URL detection
Always check if the URL is user-controlled.

## URL scheme validation
Only allow expected schemes.

## Hostname and IP validation
Validate hostnames carefully.

## Private-network blocking
Block internal IP addresses.

## Cloud metadata protection
Block 169.254.169.254 and similar.

## Redirect handling
Disable redirects or validate them.

## DNS rebinding considerations
Check DNS at resolution time.

## Timeout and response-size limits
Enforce timeouts and max response sizes.

## Network isolation
Run fetches from isolated networks if possible.

## Safe logging
Avoid logging raw URLs with credentials.

## Manual-review checklist
- [ ] Is the outbound URL user-controlled?
- [ ] Is HTTPS required?
- [ ] Is the hostname allowlisted?
- [ ] Are loopback and private IPs blocked?
- [ ] Are cloud metadata endpoints blocked?
- [ ] Are redirects disabled or revalidated?
- [ ] Is DNS resolution checked safely?
- [ ] Is there a timeout?
- [ ] Is response size limited?
- [ ] Is the server isolated from sensitive networks?
