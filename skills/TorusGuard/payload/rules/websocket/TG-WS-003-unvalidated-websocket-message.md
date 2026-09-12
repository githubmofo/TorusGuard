# TG-WS-003: Unvalidated WebSocket Message Payload

## Severity
High. Ingesting and processing incoming WebSocket message frames without schema validation or input sanitization exposes real-time backend handlers to SQL injection, XSS broadcasting, and command execution.

## Applies To
- WebSocket Message Handlers (Socket.io, ws, native WebSockets)
- Node.js, Python, Go

## Why It Matters
Unlike HTTP routes which typically have middleware validation (Zod, Joi, Pydantic), WebSocket messages frequently bypass standard middleware pipelines and pass raw client JSON directly into database queries or broadcast sinks.

## What TorusGuard Looks For
- WebSocket message event handlers directly consuming message payloads without validation schemas.

## Unsafe Example
```javascript
// UNSAFE: Consuming raw WebSocket message without schema validation
socket.on('send_message', async (data) => {
  await db.message.create({ data: { text: data.text, room: data.room } });
  io.to(data.room).emit('new_message', data);
});
```

## Safe Example
```javascript
// SAFE: Validating WebSocket payload with Zod schema before processing
const MessageSchema = z.object({
  text: z.string().min(1).max(2000),
  room: z.string().uuid()
});

socket.on('send_message', async (rawData) => {
  const result = MessageSchema.safeParse(rawData);
  if (!result.success) return socket.emit('error', 'Invalid payload schema');
  await db.message.create({ data: result.data });
  io.to(result.data.room).emit('new_message', result.data);
});
```

## Ponytail Remediation Budget
- Additions: <= 8 lines
- Deletions: <= 2 lines

## Remediation
1. Enforce validation schemas (Zod, Pydantic) on all incoming WebSocket message handlers.
2. Sanitize text fields before broadcasting to other connected clients.

## Related Rules
- `TG-INPUT-001`: Missing Server-Side Request Validation
- `TG-INPUT-003`: Unsafe Dynamic Code or HTML Execution
