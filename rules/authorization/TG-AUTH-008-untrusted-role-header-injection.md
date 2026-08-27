---
id: TG-AUTH-008
title: Untrusted Role or Tenant Header Injection
category: authentication-authorization
severity: Critical
confidence: Confirmed
frameworks:
  - django
  - drf
  - fastapi
  - flask
  - express
  - nextjs
cwe: CWE-284
asvs_v4: V4.1.1
nist_ssdf: PW.5.1
---

# TG-AUTH-008: Untrusted Role or Tenant Header Injection

## 🚨 Problem Statement
Applications that extract user roles, permissions, or tenant identifiers directly from client-supplied HTTP request headers (e.g. `X-User-Role`, `X-Tenant-ID`, `X-Is-Admin`, `X-Authenticated-User`) without cryptographic verification or a trusted API gateway boundary allow attackers to elevate privileges or access arbitrary tenant data simply by injecting custom header values.

> **Tuning Guardrails (v0.5.6):**
> - **DO NOT flag** a header merely because it is read (e.g., for logging or non-authoritative metadata).
> - **ESCALATE** only if client-controlled role/tenant data influences authorization, identity, tenant selection, or privileged database scope without verified server-side binding.
> - **DOWNGRADE** to `Needs Review` if authorization context is resolved elsewhere (e.g., API gateway, mTLS, service mesh) and cannot be proven vulnerable from local source alone.

---

## 💥 Adversarial Threat & Exploitation
An attacker sends a request with crafted HTTP headers:
```http
GET /api/v1/admin/users HTTP/1.1
Host: api.example.com
X-User-Role: superadmin
X-Tenant-ID: victim-tenant-uuid
```
If the backend application assigns permissions based on `request.headers.get("X-User-Role")` without verifying that the request originated from an internal gateway with a signed cryptographic token (or mTLS), the attacker completely bypasses authorization checks.

---

## 🛠️ Framework-Native Remediations

### 🐍 FastAPI (Dependency Injection & Signed JWT Extraction)

#### ❌ Unsafe Pattern
```python
# Unsafe: Trusting client-supplied header directly
@app.get("/admin/metrics")
async def get_metrics(x_user_role: str = Header(None)):
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"metrics": "sensitive_admin_data"}
```

#### ✅ Safe Remediation
```python
# Safe: Extracting authenticated user and roles from cryptographically verified token
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user_roles(token: str = Depends(oauth2_scheme)) -> list[str]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        return payload.get("roles", [])
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@app.get("/admin/metrics")
async def get_metrics(roles: list[str] = Depends(get_current_user_roles)):
    if "admin" not in roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return {"metrics": "sensitive_admin_data"}
```

---

### 🐍 Django / DRF (Session & Verified Token Authorization)

#### ❌ Unsafe Pattern
```python
# Unsafe: Using request header in ViewSet or middleware for tenant scoping
class DocumentViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        tenant_id = self.request.headers.get("X-Tenant-ID")
        return Document.objects.filter(tenant_id=tenant_id)
```

#### ✅ Safe Remediation
```python
# Safe: Deriving tenant isolation from authenticated user session or token claim
class DocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Derive tenant strictly from the server-authenticated user profile
        user_tenant = self.request.user.profile.tenant
        return Document.objects.filter(tenant=user_tenant)
```

---

## 🧪 Verification & Reproduction
1. Execute request with header override:
   ```bash
   curl -H "X-User-Role: admin" -H "X-Tenant-ID: victim-tenant" http://localhost:8000/api/admin/metrics
   ```
2. **Assertion:** Unauthenticated request must return `401 Unauthorized` or `403 Forbidden`, ignoring unverified header overrides.
