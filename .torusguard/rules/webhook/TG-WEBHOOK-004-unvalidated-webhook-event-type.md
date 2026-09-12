# TG-WEBHOOK-004: Unvalidated Webhook Event Type

## Severity
High. Dynamically dispatching webhook handlers using unsanitized `event.type` strings from payloads can lead to object prototype pollution, unintended method invocation, or unhandled exceptions.

## Applies To
- Dynamic Webhook Event Dispatchers
- Node.js, Python, Ruby

## Why It Matters
Using `handlers[event.type](event)` where `event.type` is controlled by the payload allows attackers to invoke object prototype properties like `toString`, `constructor`, or `__proto__`, causing crashes or prototype pollution.

## What TorusGuard Looks For
- Bracket indexing into handler objects with untrusted event type strings without allowlist validation.

## Unsafe Example
```javascript
// UNSAFE: Dynamic object lookup using unsanitized event.type
const handlers = { 'order.created': handleOrder };
app.post('/webhook', (req, res) => {
  handlers[req.body.type](req.body); // Attacker passes type: '__proto__' or 'constructor'
});
```

## Safe Example
```javascript
// SAFE: Explicit switch-case or Object.hasOwn allowlist validation
const ALLOWED_TYPES = new Set(['order.created', 'order.refunded']);
app.post('/webhook', (req, res) => {
  const { type } = req.body;
  if (!ALLOWED_TYPES.has(type)) return res.status(400).json({ error: 'Unsupported event type' });
  if (type === 'order.created') handleOrder(req.body);
});
```

## Ponytail Remediation Budget
- Additions: <= 6 lines
- Deletions: <= 2 lines

## Remediation
1. Validate event types against an explicit `Set` or `switch` statement.
2. Never dynamically execute object methods via unvetted user-controlled keys.

## Related Rules
- `TG-WEBHOOK-001`: Missing Webhook Signature Verification
- `TG-INPUT-001`: Missing Server-Side Request Validation
