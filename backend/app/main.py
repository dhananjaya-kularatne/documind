from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI # noqa: E402
from fastapi.middleware.cors import CORSMiddleware # noqa: E402
from app.routers import documents # noqa: E402

app=FastAPI(title = "DocuMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router)

@app.get("/")
def health_check():
    """Check whether the server is alive"""
    return {"status":"DocuMind API is  running"}
