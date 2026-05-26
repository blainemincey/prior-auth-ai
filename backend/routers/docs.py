"""
Serve documentation files for the in-app docs viewer.
Reads markdown files from the repo root at request time — fully offline.
"""

import os
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/docs", tags=["docs"])

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DOCS = {
    "readme":  ("README.md",       "README"),
    "runbook": ("DEMO_RUNBOOK.md", "Runbook"),
    "script":  ("DEMO_SCRIPT.md",  "Demo Script"),
}


@router.get("/{name}")
def get_doc(name: str):
    if name not in DOCS:
        raise HTTPException(status_code=404, detail=f"Doc '{name}' not found.")
    filename, title = DOCS[name]
    path = os.path.join(REPO_ROOT, filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"{filename} not found on disk.")
    return {"name": name, "title": title, "content": content}
