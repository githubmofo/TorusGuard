# TG-WS-001: Unauthenticated WebSocket Handshake

## Severity
High. Accepting WebSocket upgrade handshakes without validating authentication cookies or Bearer tokens allows unauthenticated clients to establish persistent sockets and consume server resources.

## Applies To
- `ws`, `Socket.io`, `fastapi.WebSocket`, `channels` (Django), `aiohttp`

## Why It Matters
HTTP WebSocket upgrades (`Upgrade: websocket`) begin as standard HTTP requests. If authentication is omitted during the initial HTTP upgrade:
1. Attackers can flood the server with unbounded persistent open TCP connections, exhausting socket file descriptors.
2. If authorization is deferred to post-connect messages, unauthenticated clients can linger in memory indefinitely.
3. Cross-site WebSocket hijacking (CSWSH) can occur if the `Origin` header is trusted blindly.

## What TorusGuard Looks For
1. WebSocket servers accepting the upgrade connection before validating session cookies, headers, or query tokens.
2. Missing `Origin` header validation during handshake.
3. Runtime probe: Attempting a WebSocket handshake without an `Authorization` header or session cookie; flagging if the connection status returns `101 Switching Protocols` instead of `401 Unauthorized`.

## Unsafe Example
```typescript
// UNSAFE: Accepting WebSocket upgrade without verifying session
import { WebSocketServer } from "ws";

const wss = new WebSocketServer({ port: 8080 });

wss.on("connection", (ws, req) => {
  // Handshake already succeeded without verifying authentication!
  ws.send("Welcome to real-time events");
});
```

## Safe Example
```typescript
// SAFE: Validating authentication and origin during the HTTP upgrade
import http from "http";
import { WebSocketServer } from "ws";
import { verifyJwtToken } from "./auth";

const server = http.createServer();
const wss = new WebSocketServer({ noServer: true });

server.on("upgrade", (req, socket, head) => {
  // 1. Verify Origin header
  const origin = req.headers.origin;
  if (origin !== "https://app.example.com") {
    socket.write("HTTP/1.1 403 Forbidden\r\n\r\n");
    socket.destroy();
    return;
  }

  // 2. Authenticate token before completing WebSocket handshake
  const token = req.headers["sec-websocket-protocol"] || req.headers.cookie;
  const user = verifyJwtToken(token);
  if (!user) {
    socket.write("HTTP/1.1 401 Unauthorized\r\n\r\n");
    socket.destroy();
    return;
  }

  // 3. Complete upgrade only when authenticated
  wss.handleUpgrade(req, socket, head, (ws) => {
    wss.emit("connection", ws, req, user);
  });
});
```

## Bounded Runtime Probe Protocol
When probing WebSocket endpoints under `/torusguard web-validate`:
1. Dispatch an HTTP GET request with `Upgrade: websocket` and `Connection: Upgrade` headers **without authentication credentials**.
2. Assert that the server returns `HTTP 401` or `HTTP 403` and terminates the socket.
3. If the server returns `HTTP 101 Switching Protocols`, log a high-confidence finding for unauthenticated handshake.

## Remediation
1. **Authenticate on HTTP Upgrade:** Reject unauthenticated connections with standard HTTP 401/403 status codes before calling `handleUpgrade`.
2. **Enforce Strict Origin Checking:** Validate that `req.headers.origin` matches your trusted application domain.
3. **Set Connection Timeouts:** Automatically disconnect sockets that fail message-level handshakes within 10 seconds.

## Related Rules
- `TG-WS-002`: Missing Channel-Level Authorization
- `TG-AUTH-004`: Insecure Session Cookie
- `TG-RATE-003`: Unbounded Resource Consumption
