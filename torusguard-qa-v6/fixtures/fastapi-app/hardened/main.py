from fastapi import FastAPI, Depends, HTTPException
from pydantic import HttpUrl
import httpx
from .auth import get_verified_current_user

app = FastAPI()
ALLOWED_DOMAINS = ["api.example.com"]

@app.get("/proxy")
async def fetch_url(url: HttpUrl):
    if url.host not in ALLOWED_DOMAINS:
        raise HTTPException(status_code=400, detail="Domain not allowed")
    async with httpx.AsyncClient() as client:
        res = await client.get(str(url))
    return res.text

@app.get("/admin")
async def admin_panel(current_user = Depends(get_verified_current_user)):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=403)
    return {"status": "admin_granted"}
