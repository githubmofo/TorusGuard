from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Header, HTTPException
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_secret: str = "default_secret"

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/admin/metrics")
async def get_metrics(x_role: Annotated[str, Header()] = None):
    # Untrusted header injection vulnerability
    if x_role != "admin":
        raise HTTPException(status_code=403)
    return {"metrics": "active"}
