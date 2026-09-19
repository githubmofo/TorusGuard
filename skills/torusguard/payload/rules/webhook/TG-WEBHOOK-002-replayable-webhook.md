# TG-WEBHOOK-002: Replayable Webhook Without Timestamp Validation

## Severity
Critical. Processing webhook events without verifying timestamp freshness allows an attacker with access to network logs to replay old captured webhook payloads to duplicate orders or events.

## Applies To
- Webhook Handlers (Stripe, Slack, Custom Webhooks)
- Node.js, Python, Go, Java

## Why It Matters
Even if an attacker cannot forge a cryptographic signature, they may be able to capture a valid signed request and replay it days later. Enforcing timestamp freshness (e.g. rejecting requests older than 5 minutes) neutralizes replay attacks.

## What TorusGuard Looks For
- Custom signature validation routines that verify hashes but do not check timestamp tolerances.

## Unsafe Example
```javascript
// UNSAFE: Checking signature without timestamp tolerance check
function verifySignature(payload, signature, secret) {
  const expected = crypto.createHmac('sha256', secret).update(payload).digest('hex');
  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected));
}
```

## Safe Example
```javascript
// SAFE: Asserting timestamp freshness within a 5-minute tolerance window
function verifySignature(payload, signature, timestamp, secret) {
  const now = Math.floor(Date.now() / 1000);
  if (Math.abs(now - Number(timestamp)) > 300) return false; // 5-minute tolerance
  const expected = crypto.createHmac('sha256', secret).update(`${timestamp}.${payload}`).digest('hex');
  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected));
}
```

## Ponytail Remediation Budget
- Additions: <= 6 lines
- Deletions: <= 2 lines

## Remediation
1. Include timestamp in signature computation payload (`${timestamp}.${payload}`).
2. Verify that timestamp is within a 300-second window of current server time.

## Related Rules
- `TG-WEBHOOK-001`: Missing Webhook Signature Verification
- `TG-WEBHOOK-003`: Missing Webhook Idempotency
