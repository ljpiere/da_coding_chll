# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import router as api_v1

app = FastAPI(
    title="Globant DE Challenge",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.include_router(api_v1, prefix="/api/v1")
