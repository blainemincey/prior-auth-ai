import os
import sys

# Allow running from the backend directory
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers.claims import router as claims_router
from routers.search import router as search_router
from routers.docs import router as docs_router

app = FastAPI(
    title="Healthcare Claims AI Demo",
    description=(
        "MongoDB Atlas + Voyage AI + Atlas Vector Search — "
        "operational record, embeddings, retrieval, and AI output in one platform."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origin, "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(claims_router)
app.include_router(search_router)
app.include_router(docs_router)


@app.get("/api/health")
def health():
    return {"status": "ok", "platform": "MongoDB Atlas + Voyage AI + Atlas Vector Search"}
