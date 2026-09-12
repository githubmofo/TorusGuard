# TG-WEBHOOK-001: Missing Webhook Signature Verification

## Severity
Critical. Webhook ingestion endpoints (Stripe, GitHub, Shopify) that process events without verifying HMAC cryptographic signatures allow external attackers to forge events (e.g. spoofing a `payment_intent.succeeded` event).

## Applies To
- Webhook Listeners (Express, FastAPI, Django, Flask, Next.js)
- Node.js, Python, Go, Java, C#

## Why It Matters
Webhook endpoints are public HTTP endpoints. Without signature verification, anyone who discovers the webhook URL can send forged JSON payloads mimicking payment success, account activation, or repository merges.

## What TorusGuard Looks For
- Public webhook routes (`/api/webhooks/stripe`, `/api/github-webhook`) that parse payloads without calling provider signature verification methods (`stripe.webhooks.constructEvent`, `crypto.createHmac`).

## Unsafe Example
```javascript
// UNSAFE: Trusting incoming webhook payload without verifying signature
app.post('/api/webhook/stripe', express.json(), async (req, res) => {
  const event = req.body;
  if (event.type === 'payment_intent.succeeded') {
    await fulfillOrder(event.data.object.metadata.orderId);
  }
  res.json({ received: true });
});
```

## Safe Example
```javascript
// SAFE: Verifying Stripe HMAC signature using raw request body
app.post('/api/webhook/stripe', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['stripe-signature'];
  let event;
  try {
    event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }
  if (event.type === 'payment_intent.succeeded') {
    fulfillOrder(event.data.object.metadata.orderId);
  }
  res.json({ received: true });
});
```

## Ponytail Remediation Budget
- Additions: <= 12 lines
- Deletions: <= 4 lines

## Remediation
1. Use raw request body buffer for signature computation.
2. Verify signatures using provider SDKs or timing-safe HMAC comparison (`crypto.timingSafeEqual`).
3. Store webhook signing secrets in environment variables (`STRIPE_WEBHOOK_SECRET`).

## Related Rules
- `TG-WEBHOOK-002`: Replayable Webhook Without Timestamp Validation
- `TG-WEBHOOK-003`: Missing Webhook Idempotency
