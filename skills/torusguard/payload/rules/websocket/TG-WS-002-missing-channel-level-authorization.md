# TG-WS-002: Missing Channel-Level WebSocket Authorization

## Severity
Critical. Allowing WebSocket clients to subscribe to rooms, topics, or channels (`socket.join(...)`) without verifying that the client has permission to view that channel leaks real-time private messages across tenants.

## Applies To
- Real-Time Sockets (Socket.io, ws, ActionCable, Django Channels)
- Node.js, Python, Go

## Why It Matters
In real-time chat or multi-tenant collaboration applications, joining a room grants immediate broadcast reception. If a client can emit `join_room("tenant_123_finance")` and the server joins them without verifying membership, all private room broadcasts leak.

## What TorusGuard Looks For
- Socket event listeners (`socket.on('join')`) that join rooms based on client input without permissions checks.

## Unsafe Example
```javascript
// UNSAFE: Joining channel directly from client parameter without auth check
io.on('connection', (socket) => {
  socket.on('join_channel', (channelId) => {
    socket.join(channelId); // Attacker joins other tenants' private channels
  });
});
```

## Safe Example
```javascript
// SAFE: Verifying tenant membership before allowing channel join
io.on('connection', (socket) => {
  socket.on('join_channel', async (channelId) => {
    const isMember = await checkChannelAccess(socket.data.user.id, channelId);
    if (!isMember) return socket.emit('error', 'Unauthorized channel access');
    socket.join(channelId);
  });
});
```

## Ponytail Remediation Budget
- Additions: <= 6 lines
- Deletions: <= 2 lines

## Remediation
1. Attach authenticated user session data to the socket during handshake (`socket.data.user`).
2. Verify user channel membership against database before calling `socket.join(channelId)`.

## Related Rules
- `TG-WS-001`: Unauthenticated WebSocket Handshake
- `TG-DB-004`: Missing Multi-Tenant Query Isolation
