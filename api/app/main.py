from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, me, issues, public
from app.core.config import settings
from app.core.db import init_db

app = FastAPI(title="Civic Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(me.router, tags=["me"])
app.include_router(issues.router, prefix="/issues", tags=["issues"])
app.include_router(public.router, prefix="/public", tags=["public"])

@app.get("/healthz")
def healthz():
    return {"status": "ok", "env": settings.APP_ENV}

@app.on_event("startup")
def on_startup():
    init_db()
