# FastAPI Rule Verification Matrix (TorusGuard v0.4.0)

| Rule ID | Rule Title | Test Target File | Detection Check | Expected Result | Confidence |
|---|---|---|---|---|:---:|
| `TG-SSRF-001` | Unvalidated URL Fetch | `main.py` | `requests.get(url)` without scheme/host validation | Flagged as SSRF Risk | Confirmed |
| `TG-WEBHOOK-001` | Missing Signature Validation | `main.py` | POST webhook parses payload without HMAC verification | Flagged as Insecure Webhook | Confirmed |
| `TG-AUTH-006` | Mass Assignment | `main.py` | Endpoint accepts raw `dict` without Pydantic model | Flagged as Mass Assignment Risk | Confirmed |
