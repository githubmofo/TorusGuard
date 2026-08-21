# Regression Fixture: Unsafe Outbound URL Fetch (SSRF)

- **Framework:** FastAPI / Python
- **Target Rule:** `TG-SSRF-001`
- **Expected Classification:** `Confirmed`
- **Expected Rule IDs:** `TG-SSRF-001`
- **Reasoning:** Route accepts arbitrary user-supplied URL and executes `httpx.get(target_url)` without validating hostname, IP addresses, or blocking private subnets.

## Sample Code
```python
import httpx

async def fetch_user_webhook(target_url: str):
    # VULNERABLE: Direct outbound request to untrusted URL
    async with httpx.AsyncClient() as client:
        return await client.get(target_url)
```
