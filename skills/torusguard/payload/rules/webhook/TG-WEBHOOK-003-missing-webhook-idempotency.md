# TG-WEBHOOK-003: Missing Webhook Idempotency

## Severity
High. Processing incoming webhook events without recording event IDs allows duplicate webhook delivery to trigger duplicate fulfillments, charges, or database entries.

## Applies To
- Webhook Event Handlers
- Node.js, Python, Go, Java, C#

## Why It Matters
Webhook providers (Stripe, GitHub, PayPal) employ retry mechanisms and guarantee *at-least-once* delivery. If a network blip causes your server to respond slowly, the provider resends the webhook. Without idempotency checks, actions execute multiple times.

## What TorusGuard Looks For
- Event handlers executing side-effects immediately without checking if `event.id` was already processed.

## Unsafe Example
```javascript
// UNSAFE: Handling event without deduplicating by event ID
app.post('/api/webhook', async (req, res) => {
  const event = req.event;
  await creditUserAccount(event.userId, event.amount); // Executed on every retry
  res.sendStatus(200);
});
```

## Safe Example
```javascript
// SAFE: Recording processed event IDs to guarantee idempotency
app.post('/api/webhook', async (req, res) => {
  const event = req.event;
  const exists = await db.processedEvent.findUnique({ where: { id: event.id } });
  if (exists) return res.status(200).json({ status: 'already_processed' });
  await db.$transaction([
    db.processedEvent.create({ data: { id: event.id } }),
    creditUserAccount(event.userId, event.amount)
  ]);
  res.sendStatus(200);
});
```

## Ponytail Remediation Budget
- Additions: <= 8 lines
- Deletions: <= 3 lines

## Remediation
1. Store processed event IDs in a persistent table with unique constraints.
2. Return 200 OK immediately if an event ID has already been recorded.

## Related Rules
- `TG-BIZ-002`: Replayable One-Time Operation
- `TG-WEBHOOK-001`: Missing Webhook Signature Verification
