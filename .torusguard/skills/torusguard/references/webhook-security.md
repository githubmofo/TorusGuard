# Webhook Security

- Signature verification over the raw request body.
- Timestamp tolerance.
- Replay protection.
- Event-type allowlisting.
- Payload schema validation.
- Idempotency keys or event IDs.
- Safe retry behavior.
- Rate and size limits.
- Generic response errors.
- No trust in event fields before signature verification.

## Workflow
Receive raw body → Verify signature → Verify timestamp → Check event ID/idempotency → Validate event schema → Authorize event source/tenant → Process within transaction → Return safe response
