from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from services.api.models import SessionLocal
from services.api.crud import search_jobs, update_application

app = FastAPI(title="Internship Tracker Pro", version="1.0")

origins = [os.getenv("FRONTEND_ORIGIN","http://localhost:5173"), "http://127.0.0.1:5173"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class ApplicationPatch(BaseModel):
    applied: Optional[bool] = None
    saved: Optional[bool] = None
    notes: Optional[str] = None
    cold_email_sent: Optional[bool] = None

@app.get("/health")
def health(): return {"ok": True}

@app.get("/jobs")
def jobs(q: Optional[str] = None, source: Optional[str] = None, applied: Optional[bool] = None, limit: int = Query(50, le=200), offset:int = 0):
    with SessionLocal() as db:
        return search_jobs(db, q, source, applied, limit, offset)

@app.patch("/jobs/{job_id}/application")
def patch(job_id:int, body: ApplicationPatch):
    with SessionLocal() as db:
        res = update_application(db, job_id, body.dict())
        if not res.get("ok"): raise HTTPException(404, res.get("error","error"))
        return res
