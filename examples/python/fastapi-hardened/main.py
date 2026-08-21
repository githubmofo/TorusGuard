import ipaddress
import socket
import hmac
import hashlib
from urllib.parse import urlparse
from fastapi import FastAPI, HTTPException, Header, Request
from pydantic import BaseModel, Field
import requests

app = FastAPI()

WEBHOOK_SECRET = b"test_secret_for_local_verification_only"

def is_safe_url(target_url: str) -> bool:
    try:
        parsed = urlparse(target_url)
        if parsed.scheme not in ("http", "https"):
            return False
        ip_str = socket.gethostbyname(parsed.hostname)
        ip = ipaddress.ip_address(ip_str)
        return not (ip.is_loopback or ip.is_private or ip.is_link_local or ip.is_reserved)
    except Exception:
        return False

# ✅ TG-SSRF-001: Safe URL fetch
@app.get("/fetch")
def fetch_url(url: str):
    if not is_safe_url(url):
        raise HTTPException(status_code=400, detail="Invalid destination address")
    response = requests.get(url, timeout=5)
    return {"status": response.status_code, "content": response.text}

# ✅ TG-WEBHOOK-001: Verified webhook
@app.post("/webhook")
async def receive_webhook(request: Request, x_signature: str = Header(None)):
    if not x_signature:
        raise HTTPException(status_code=400, detail="Missing signature header")
    body = await request.body()
    expected = hmac.new(WEBHOOK_SECRET, body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, x_signature):
        raise HTTPException(status_code=403, detail="Invalid webhook signature")
    return {"status": "success"}

class ProfileUpdateSchema(BaseModel):
    display_name: str = Field(..., min_length=1, max_length=50)
    bio: str | None = Field(None, max_length=200)

    class Config:
        extra = "forbid"

# ✅ TG-AUTH-006: Explicit schema
@app.post("/update_profile")
def update_profile(user_id: int, payload: ProfileUpdateSchema):
    return {"status": "updated", "user_id": user_id, "data": payload.dict()}
