# FastAPI Security Guide (TorusGuard v0.4.0)

> **Scope:** Security standards for FastAPI applications. Covers Pydantic v2 validation, dependency-based authentication and authorization, ownership scoping, SSRF protection with HTTP clients, webhook signatures, and production OpenAPI documentation exposure.

---

## 🔍 Scope and Detection
TorusGuard detects FastAPI applications when `from fastapi import FastAPI`, `FastAPI()`, or `fastapi` in dependency files is present.

---

## 🛡️ 1. Authentication & Authorization Dependencies (`TG-AUTH-001`, `TG-AUTH-003`)

FastAPI uses dependency injection (`Depends`) to enforce authentication and authorization at the route or router level.

### Safe Pattern
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    user = verify_jwt_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Enforce authorization check
def require_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted",
        )
    return current_user
```

---

## 👤 2. Object Ownership & Tenant Scoping (`TG-AUTH-007`)

Never fetch database records solely by path parameter without verifying tenant or user ownership.

### ❌ Unsafe Pattern
```python
# VULNERABLE: Any authenticated caller can view any profile by ID
@app.get("/profiles/{profile_id}")
async def get_profile(profile_id: int, current_user: User = Depends(get_current_user)):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    return profile
```

### ✅ Safe Pattern
```python
# SAFE: Scope lookup strictly to current user's profile
@app.get("/profiles/{profile_id}")
async def get_profile(profile_id: int, current_user: User = Depends(get_current_user)):
    profile = db.query(Profile).filter(
        Profile.id == profile_id, 
        Profile.user_id == current_user.id
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
```

---

## 📝 3. Pydantic Request Models & Mass Assignment (`TG-AUTH-006`)

Always define explicit Pydantic request models rather than accepting raw dictionaries (`dict`) or unpacking arbitrary client fields into ORM models.

### ❌ Unsafe Pattern
```python
# VULNERABLE: Accepts arbitrary dict updates directly into database
@app.post("/users/{user_id}/update")
async def update_user(user_id: int, updates: dict):
    # Attacker can send {"is_admin": True, "wallet_balance": 99999}
    db.query(User).filter(User.id == user_id).update(updates)
```

### ✅ Safe Pattern
```python
# SAFE: Define strict Pydantic schema with allowed fields only
class UserUpdateSchema(BaseModel):
    display_name: str
    bio: str | None = None

    class Config:
        extra = "forbid"  # Reject unexpected fields

@app.post("/users/{user_id}/update")
async def update_user(
    user_id: int, 
    payload: UserUpdateSchema, 
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    user.display_name = payload.display_name
    user.bio = payload.bio
    db.commit()
    return user
```

---

## 🌐 4. Server-Side Request Forgery (SSRF) (`TG-SSRF-001`, `TG-SSRF-002`)

When fetching external URLs (via `httpx`, `requests`, or `aiohttp`), validate the scheme, hostname, and resolved IP to block access to internal private subnets and cloud metadata services (`169.254.169.254`).

```python
import ipaddress
import socket
from urllib.parse import urlparse
import httpx

def is_safe_url(target_url: str) -> bool:
    parsed = urlparse(target_url)
    if parsed.scheme not in ("http", "https"):
        return False
    
    # Resolve hostname to IP
    ip_str = socket.gethostbyname(parsed.hostname)
    ip = ipaddress.ip_address(ip_str)
    
    # Block loopback, private, link-local, and reserved ranges
    if ip.is_loopback or ip.is_private or ip.is_link_local or ip.is_reserved:
        return False
    return True
```

---

## 🪝 5. Webhook Signature Verification (`TG-WEBHOOK-001`)

Verify HMAC signatures using the raw request body before parsing JSON payloads.

```python
import hmac
import hashlib
from fastapi import Request, Header

@app.post("/webhooks/stripe")
async def receive_stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None)
):
    raw_body = await request.body()
    # Verify signature using constant-time comparison
    expected = hmac.new(WEBHOOK_SECRET, raw_body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, stripe_signature):
        raise HTTPException(status_code=400, detail="Invalid webhook signature")
    return {"status": "success"}
```

---

## 📋 Manual Review Checklist for FastAPI

- [ ] Route dependencies enforce authentication and role/scope authorization.
- [ ] Object lookups filter by `current_user.id` or account/tenant ID.
- [ ] Pydantic models forbid unexpected fields (`extra = "forbid"`).
- [ ] Outbound HTTP fetches validate target IP addresses and block private CIDR blocks.
- [ ] Webhook endpoints verify signatures against raw request bytes.
- [ ] In production, interactive documentation (`/docs`, `/redoc`) is disabled or access-restricted.
