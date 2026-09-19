# TG-WS-004: Unbounded WebSocket Connections & Rate Limiting

## Severity
Medium. Permitting unlimited concurrent WebSocket connections per IP address or user allows attackers to exhaust file descriptors, socket memory pools, and server CPU via connection flood attacks.

## Applies To
- WebSocket Servers (ws, Socket.io, Django Channels, Gorilla WebSocket)
- Node.js, Python, Go

## Why It Matters
WebSocket connections are persistent TCP connections that remain open. Without connection throttling or message rate limits, a single client can open 10,000 idle sockets, consuming all available file descriptors and denying service to legitimate users.

## What TorusGuard Looks For
- WebSocket server configurations lacking maximum connection limits, per-IP socket caps, or message throttling.

## Unsafe Example
```javascript
// UNSAFE: Accepting unbounded WebSocket connections without rate limiting
const wss = new WebSocketServer({ port: 8080 });
```

## Safe Example
```javascript
// SAFE: Enforcing per-IP connection limits and message rate bounds
const ipConnections = new Map();
const MAX_CONNS_PER_IP = 10;

server.on('upgrade', (req, socket, head) => {
  const ip = req.socket.remoteAddress;
  const count = ipConnections.get(ip) || 0;
  if (count >= MAX_CONNS_PER_IP) {
    socket.destroy();
    return;
  }
  ipConnections.set(ip, count + 1);
  socket.on('close', () => ipConnections.set(ip, Math.max(0, (ipConnections.get(ip) || 1) - 1)));
});
```

## Ponytail Remediation Budget
- Additions: <= 10 lines
- Deletions: <= 2 lines

## Remediation
1. Enforce per-IP connection limits in the HTTP `upgrade` request listener.
2. Implement heartbeat ping/pong timeouts to terminate dead or idle sockets.
3. Throttle inbound message rates using token bucket or sliding window algorithms.

## Related Rules
- `TG-RATE-003`: Unbounded Resource Consumption
- `TG-WS-001`: Unauthenticated WebSocket Handshake
