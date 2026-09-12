# TG-BIZ-002: Replayable One-Time Operation

## Severity
High. Lack of idempotent tokens, nonces, or single-use consumption flags allows attackers or network retries to execute financial charges, coupon redemptions, or password resets multiple times.

## Applies To
- Coupon Redemptions, Financial Transfers, Voucher APIs, Password Reset Consumptions
- Node.js, Python, Go, Java, C#

## Why It Matters
Transient network glitches, automated retry loops, or intentional race condition attacks (TOCTOU) can submit duplicate requests. Without single-use atomic locking, a user can redeem a $50 gift card 10 times concurrently.

## What TorusGuard Looks For
- State-changing transaction handlers lacking idempotency keys, single-use nonce validation, or atomic database lock transactions (`SELECT ... FOR UPDATE`).

## Unsafe Example
```python
# UNSAFE: Checking balance and deducting without atomic idempotency lock
@app.post("/api/redeem-coupon")
def redeem_coupon(code: str, user_id: str):
    coupon = db.query(Coupon).filter_by(code=code, used=False).first()
    if coupon:
        apply_credit(user_id, coupon.amount)
        coupon.used = True
        db.commit()
```

## Safe Example
```python
# SAFE: Atomic database update with idempotency check
@app.post("/api/redeem-coupon")
def redeem_coupon(code: str, user_id: str, idempotency_key: str):
    with db.begin():
        rows = db.query(Coupon).filter_by(code=code, used=False).update({"used": True})
        if rows == 0:
            raise HTTPException(status_code=400, detail="Coupon already redeemed")
        apply_credit(user_id, coupon.amount)
```

## Ponytail Remediation Budget
- Additions: <= 14 lines
- Deletions: <= 5 lines

## Remediation
1. Require an `Idempotency-Key` header on all sensitive mutations.
2. Execute state-changing consumption operations inside atomic database transactions with row-level locks.
3. Mark vouchers or tokens as `consumed` in the same atomic operation before dispatching external side-effects.

## Verification
- Send 5 concurrent identical redemption requests with the same coupon code; assert exactly 1 succeeds (200 OK) and 4 fail (400/409 Conflict).

## Related Rules
- `TG-WEBHOOK-003`: Missing Webhook Idempotency
- `TG-BIZ-003`: Missing Workflow State Validation
