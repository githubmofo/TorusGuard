from fastapi import FastAPI, Header, HTTPException
import httpx

app = FastAPI()

@app.get("/proxy")
async def fetch_url(url: str):
    # SSRF: Unvalidated outbound HTTP destination
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
    return res.text

@app.get("/admin")
async def admin_panel(x_user_role: str = Header(None)):
    # Insecure Header Trust
    if x_user_role != "admin":
        raise HTTPException(status_code=403)
    return {"status": "admin_granted"}
