from fastapi import FastAPI
import requests

app = FastAPI()

# ❌ TG-SSRF-001: Unvalidated outbound URL fetching
@app.get("/fetch")
def fetch_url(url: str):
    response = requests.get(url)
    return {"status": response.status_code, "content": response.text}

# ❌ TG-WEBHOOK-001: Unverified webhook payload
@app.post("/webhook")
def receive_webhook(payload: dict):
    return {"status": "success", "data": payload}

# ❌ TG-AUTH-006: Unfiltered dict mass assignment
@app.post("/update_profile")
def update_profile(user_id: int, updates: dict):
    return {"status": "updated", "user_id": user_id, "updates": updates}
