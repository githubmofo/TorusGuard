# TG-BIZ-003: Missing Workflow State Validation

## Severity
High. Skipping validation of intermediate business lifecycle states allows users to bypass mandatory verification, payment, or approval steps.

## Applies To
- Order Processing, Multi-Step Onboarding, Approval Pipelines, KYC Verification
- Node.js, Python, Go, Java, C#

## Why It Matters
When endpoints assume prerequisite stages were completed without strictly querying the current entity state, malicious actors can invoke late-stage endpoints directly (e.g. calling `/api/orders/{id}/fulfill` on an order whose state is `PENDING_PAYMENT`).

## What TorusGuard Looks For
- State transitions (`status = 'SHIPPED'`, `status = 'APPROVED'`) executed without asserting that current status matches required prior state (`where: { status: 'PAID' }`).

## Unsafe Example
```javascript
// UNSAFE: Transitioning order to fulfilled without checking current status
app.post('/api/orders/:id/fulfill', async (req, res) => {
  await db.order.update({
    where: { id: req.params.id },
    data: { status: 'FULFILLED' }
  });
});
```

## Safe Example
```javascript
// SAFE: Atomic conditional transition verifying prerequisite state
app.post('/api/orders/:id/fulfill', async (req, res) => {
  const result = await db.order.updateMany({
    where: { id: req.params.id, status: 'PAID' },
    data: { status: 'FULFILLED' }
  });
  if (result.count === 0) return res.status(400).json({ error: 'Order not ready for fulfillment' });
});
```

## Ponytail Remediation Budget
- Additions: <= 10 lines
- Deletions: <= 4 lines

## Remediation
1. Define a strict state machine with allowable transitions.
2. Enforce atomic conditional updates asserting the expected source state.
3. Return 400 or 409 errors when an invalid transition is attempted.

## Verification
- Attempt to fulfill an unpaid order; confirm 400 rejection.

## Related Rules
- `TG-BIZ-001`: Client-Controlled Sensitive Business Value
- `TG-AUTH-003`: Missing Object-Level Authorization
