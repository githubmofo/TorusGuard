# Remediation Mapping: FastAPI Vulnerable -> Hardened

| Vulnerability | Rule ID | Vulnerable File | Hardened File | Security Control Applied |
|---|---|---|---|---|
| Unrestricted URL Fetch (SSRF) | `TG-SSRF-001` | `main.py` | `main.py` | DNS resolution check & private IP blocklist |
| Unverified Webhook Endpoint | `TG-WEBHOOK-001` | `main.py` | `main.py` | Constant-time HMAC-SHA256 signature verification |
| Mass Assignment / Unfiltered Dict | `TG-AUTH-006` | `main.py` | `main.py` | Strict Pydantic schema with `extra="forbid"` |
| Object Ownership IDOR | `TG-AUTH-007` | `main.py` | `main.py` | Authenticated user session & ownership query scoping |
