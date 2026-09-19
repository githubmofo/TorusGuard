# TG-BIZ-001: Client-Controlled Sensitive Business Value

## Severity
Critical. Relying on client-submitted values for critical financial, authorization, or pricing attributes allows malicious users to manipulate monetary amounts, discounts, or permissions.

## Applies To
- E-Commerce Checkout, Payment Handlers, Subscription APIs
- Node.js (Express, NestJS, Next.js), Python (FastAPI, Django, Flask), Go, Java, C#

## Why It Matters
When client requests directly dictate sensitive pricing or balance fields (such as `amount`, `unit_price`, `discount_percent`, or `credit_balance`), attackers can tamper with request payloads to purchase items at arbitrary prices ($0.01) or grant themselves unearned credits.

## What TorusGuard Looks For
- Destructuring sensitive price or discount attributes directly from `req.body` or `request.data` into payment gateways or order creation queries.
- Absence of server-side database lookup for product prices prior to charge generation.

## Unsafe Example
```javascript
// UNSAFE: Directly trusting price and amount from client payload
app.post('/api/checkout', async (req, res) => {
  const { productId, price, quantity } = req.body;
  const total = price * quantity; // Attacker sends price: 0.01
  await paymentGateway.charge({ amount: total });
});
```

## Safe Example
```javascript
// SAFE: Fetching canonical price from authoritative server database
app.post('/api/checkout', async (req, res) => {
  const { productId, quantity } = req.body;
  const product = await db.product.findUnique({ where: { id: productId } });
  if (!product) return res.status(404).json({ error: 'Product not found' });
  const total = product.price * quantity;
  await paymentGateway.charge({ amount: total });
});
```

## Ponytail Remediation Budget
- Additions: <= 12 lines
- Deletions: <= 4 lines

## Remediation
1. Remove sensitive pricing and discount parameters from incoming client request schemas.
2. Query the authoritative server database or catalog for the verified unit price.
3. Calculate subtotal, taxes, and final charge amounts exclusively on the trusted server.

## Verification
- Submit a checkout payload with `price: 0.01` and verify the server rejects or ignores the parameter and bills the canonical catalog price.

## Related Rules
- `TG-INPUT-001`: Missing Request Body Validation Schema
- `TG-BIZ-004`: Unrestricted Sensitive Business Workflow
