# Real-World Validation Record: FastAPI Application

- **Repository:** Anonymized FastAPI Asynchronous Notification & Webhook Gateway
- **Authorization:** Maintainer-permitted code review evaluation
- **Repository Version / Commit SHA:** `8a1f3c7e92b4d06a5e8c2f1a4b6d9e3c7f1a5b89`
- **Stack Detected:** Python 3.12, FastAPI 0.110, Pydantic v2, `httpx`, `pyproject.toml` (uv)
- **TorusGuard Version:** v0.4.0
- **Date Tested:** 2026-08-21

---

## 🔍 Findings

| Rule ID | Classification | Evidence | Maintainer Outcome |
|---|---|---|---|
| `TG-SSRF-001` | **Confirmed** | Callback dispatcher invoked `httpx.AsyncClient().post(customer_url)` without checking for internal IP ranges | **Confirmed & Remediated:** Implemented DNS resolution and private CIDR blocklist (`10.0.0.0/8`, `169.254.0.0/16`, `127.0.0.1`). |
| `TG-WEBHOOK-001` | **Manual Review** | Inbound webhook route used JSON body parsing before verifying signature header | **Confirmed & Remediated:** Refactored to read `await request.body()` for raw byte HMAC comparison. |
| `TG-AUTH-006` | **Informational** | Pydantic v2 schemas used default extra field behavior | **Remediated:** Added `model_config = ConfigDict(extra='forbid')` to all ingestion schemas. |

---

## 📊 Results Summary

- **Confirmed Findings:** 1 (Outbound webhook SSRF)
- **Manual Review Findings:** 1 (Webhook raw body signature verification)
- **Informational Findings:** 1 (Pydantic extra fields config)
- **False Positives:** 0
- **Rule Wording Improvements:** Emphasized in `TG-WEBHOOK-001` that HMAC signatures must compute against raw request payload bytes rather than re-serialized JSON.
