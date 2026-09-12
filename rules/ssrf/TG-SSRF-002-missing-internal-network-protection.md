# TG-SSRF-002: Missing Internal Network Protection

## Severity
Critical. Allowing server-side HTTP clients to dispatch requests to internal network interfaces (127.0.0.1, private RFC 1918 subnets, or cloud metadata services like 169.254.169.254) allows external attackers to extract cloud credentials and interact with internal microservices.

## Applies To
- Webhook dispatchers, URL preview fetchers, PDF generators, image proxies
- Node.js (fetch, axios), Python (requests, httpx, urllib), Go (net/http), Java

## Why It Matters
If a server accepts a destination URL from a user (e.g. `/api/fetch-avatar?url=...`) without blocking private network spaces, an attacker can supply `http://169.254.169.254/latest/meta-data/iam/security-credentials/` to steal AWS IAM role tokens, or `http://127.0.0.1:6379` to inject Redis commands.

## What TorusGuard Looks For
- Server-side request calls dispatching requests to unvalidated URLs that could resolve to loopback (`127.0.0.0/8`), link-local (`169.254.0.0/16`), or private IP ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`).

## Unsafe Example
```python
# UNSAFE: Outbound fetch without private IP filtering
import requests
from fastapi import FastAPI

app = FastAPI()

@app.get("/fetch")
def fetch_url(url: str):
    return requests.get(url).text # Attacker passes http://169.254.169.254/...
```

## Safe Example
```python
# SAFE: Resolving IP and validating against private subnet ranges before fetching
import socket
import ipaddress
import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

def is_safe_url(url: str) -> bool:
    from urllib.parse import urlparse
    hostname = urlparse(url).hostname
    if not hostname: return False
    ip = ipaddress.ip_address(socket.gethostbyname(hostname))
    return not (ip.is_private or ip.is_loopback or ip.is_link_local)

@app.get("/fetch")
def fetch_url(url: str):
    if not is_safe_url(url):
        raise HTTPException(status_code=400, detail="Invalid destination IP")
    return requests.get(url, timeout=5.0).text
```

## Ponytail Remediation Budget
- Additions: <= 14 lines
- Deletions: <= 2 lines

## Remediation
1. Parse the destination hostname and resolve DNS.
2. Assert that resolved IP addresses are neither loopback (`127.0.0.0/8`), link-local (`169.254.0.0/16`), nor RFC 1918 private subnets.
3. Pin DNS resolution to prevent time-of-check to time-of-use (TOCTOU) DNS rebinding attacks.

## Related Rules
- `TG-SSRF-001`: User-Controlled Server-Side URL Fetch
- `TG-SSRF-004`: Unbounded Outbound Request
