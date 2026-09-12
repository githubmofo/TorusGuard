# TorusGuard v0.4.0 Validation Report: FastAPI

> **Target:** FastAPI Reference Application (`examples/python/fastapi-vuln/`)  
> **Framework:** FastAPI 0.110+ / Pydantic v2  
> **Test Mode:** Local Simulated `/torusguard audit` & `/torusguard harden`  
> **Status:** Validation Completed Successfully  

---

> 🛡️ **TorusGuard Validation Heritage:** This document preserves empirical validation records for this framework and milestone. For the current v1.3.5 active release line, 74-rule AST engine, living security report ground truth (`security_report.md`), and automated test suite (81/81 passing via `npm test`), refer to the [Validation Suite Overview](README.md) and root [README](../../README.md).


## 🎯 1. Test Scope & Purpose
Validate TorusGuard rules against FastAPI asynchronous patterns, Pydantic schemas, outbound requests (SSRF), and webhook signature verification.

---

## 🔍 2. Verified Findings

### 🔴 1. Server-Side Request Forgery / Unvalidated Outbound Fetch (`TG-SSRF-001`)
* **Classification:** `Confirmed`
* **Evidence:** `main.py` passes user-controlled `url` query string directly to `requests.get(url)`.
* **Impact:** Callers can probe internal metadata endpoints (`http://169.254.169.254/latest/meta-data/`) or private microservices.
* **Remediation:** Implement DNS hostname resolution check, protocol whitelist (`http`, `https`), and private IP range blocklist.

### 🔴 2. Unauthenticated Webhook Endpoint (`TG-WEBHOOK-001`)
* **Classification:** `Confirmed`
* **Evidence:** `POST /webhook` processes incoming payloads without verifying HMAC signatures.
* **Impact:** Attackers can forge arbitrary webhook events (e.g. fake payment confirmations).
* **Remediation:** Require `X-Signature` header and verify using `hmac.compare_digest()` on raw request bytes.

### 🟠 3. Mass Assignment via Raw Dict (`TG-AUTH-006`)
* **Classification:** `Confirmed`
* **Evidence:** `POST /update_profile` accepts an unrestricted `dict` type payload.
* **Impact:** Uncontrolled parameters can be passed into downstream database persistence layers.
* **Remediation:** Define strict Pydantic `BaseModel` with `extra = "forbid"`.

---

## ⚖️ 3. Validation Limitations
- Validated on local test target; external network topologies and cloud metadata firewalls require infrastructure-level review.
