from pathlib import Path
import shutil

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

BUILD_DIR = Path(__file__).resolve().parents[1] / "build"


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # Save incoming file to tools/uploads and return its server path.
    dest = UPLOAD_DIR / (file.filename or "upload.ply")
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    return JSONResponse({"ok": True, "filename": dest.name, "path": str(dest)})


@app.get("/")
async def root():
    return {"ok": True, "message": "Upload server ready", "upload": "/upload", "build": "/build"}


app.mount("/build", StaticFiles(directory=str(BUILD_DIR)), name="build")
