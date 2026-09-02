# Business Logic and Abuse

## Topics
- Coupon and discount abuse.
- Trial and referral abuse.
- Payment amount tampering.
- Inventory manipulation.
- OTP and verification workflow bypass.
- Vote and rating manipulation.
- Repeated one-time operations.
- AI or third-party API cost abuse.
- Replay and idempotency.
- Per-user and per-account velocity.
- Server-side state transitions.

## Review Table
| Flow | Value protected | Abuse action | Existing control | Missing control |
|---|---|---|---|---|
| Apply coupon | Discount amount | Reuse coupon | Database flag | Atomic update |
| Send OTP | SMS cost | Repeated requests | IP limiter | Account limiter |
| Create order | Inventory/payment | Modify quantity/price | Auth only | Server-side pricing |

The agent must ask whether a user can execute a technically valid operation too many times. OWASP identifies sensitive business-flow abuse separately from ordinary authentication and resource-exhaustion concerns.
