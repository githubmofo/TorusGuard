# TG-SSRF-004: Unbounded Outbound Request Without Timeout

## Severity
Critical. Dispatching server-side HTTP requests without strict socket and read timeouts allows malicious endpoints or slowloris servers to hang server worker threads indefinitely, leading to resource exhaustion and DoS.

## Applies To
- Outbound HTTP Clients (Python `requests`, Node `axios`, Go `http.Client`)
- Python, Node.js, Go, Java

## Why It Matters
In Python `requests`, the default timeout is `None` (it waits forever). If an attacker provides a URL pointing to a server that accepts the connection and trickles 1 byte every 10 minutes, your server worker threads become permanently exhausted.

## What TorusGuard Looks For
- Outbound HTTP calls (`requests.get`, `requests.post`, `axios.get`, `fetch`) lacking explicit `timeout` parameters.

## Unsafe Example
```python
# UNSAFE: Python requests call without timeout hangs indefinitely
import requests

def fetch_avatar(url: str):
    response = requests.get(url) # Can hang indefinitely
    return response.content
```

## Safe Example
```python
# SAFE: Explicit timeout prevents hanging worker threads
import requests

def fetch_avatar(url: str):
    response = requests.get(url, timeout=5.0) # 5-second socket timeout
    return response.content
```

## Ponytail Remediation Budget
- Additions: <= 2 lines
- Deletions: <= 1 line

## Remediation
1. Always specify an explicit `timeout` on all network calls (typically 3.0 to 10.0 seconds).
2. Configure custom client sessions with default timeouts applied globally.

## Related Rules
- `TG-SSRF-001`: User-Controlled Server-Side URL Fetch
- `TG-RATE-003`: Unbounded Resource Consumption
