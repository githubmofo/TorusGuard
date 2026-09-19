# Rate Limiting and Abuse Prevention

## When to load

Load during `/TorusGuard check rate-limit`, auth endpoint reviews, or public API design.

## Linked rules

- [TG-RATE-001](../../rules/TG-RATE-001-unlimited-auth-endpoint.md) — Unlimited Auth Endpoint (High)
- [TG-RATE-002](../../rules/TG-RATE-002-unlimited-public-write-endpoint.md) — Unlimited Public Write (Medium)
- [TG-RATE-003](../../rules/TG-RATE-003-unbounded-resource-consumption.md) — Unbounded Resource Use (High)

## Hard bans

- Never rely only on frontend throttling
- Never leave login, reset, OTP, or contact endpoints unlimited in production
- Never use in-memory-only rate limits as sole protection in distributed production

## Configurable default limits

| Endpoint | Suggested starting point |
|----------|-------------------------|
| Login | 5 / IP / 15 min + account backoff |
| Password reset | 3 / email / hour |
| OTP | 3 / identifier / 15 min |
| Contact/feedback | 5 / IP / hour |
| Public API | 60 / IP / minute |
| Search | 30 / IP / minute |
| Upload | 10 / IP / hour + size limits |
| AI/LLM | Per-user and per-IP cost limits |

Adjust for your traffic profile — these are defaults, not universal values.

## Safe defaults

- Per-IP limits on public endpoints
- Per-account limits on auth flows
- HTTP 429 with `Retry-After` when practical
- Body, upload, and pagination caps (TG-RATE-003)
- Timeouts and concurrency limits on expensive endpoints
- Shared store (Redis) for multi-instance deployments

## Audit checklist

- [ ] Auth endpoints rate-limited (TG-RATE-001)
- [ ] Public write/AI endpoints protected (TG-RATE-002)
- [ ] Body/upload/pagination limits set (TG-RATE-003)

## Manual review

- Webhook endpoints (signature + IP limits)
- GraphQL complexity/depth limits
- Spend alerts for metered third-party APIs

## Related rules

TG-AUTH-005, TG-PLATFORM-004, TG-INPUT-004
