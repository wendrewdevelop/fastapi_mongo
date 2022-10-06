import requests
import uvicorn
from pymongo import errors
from typing import Any, List, Optional
from fastapi import (
    FastAPI, 
    Path, 
    Request, 
    status, 
    Query
)
from fastapi.responses import JSONResponse
from app import schema
from bootstrap import mongodb
from app.validators import CepNotFoundException
from app.config import app
from app.routes import router as api_router


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="localhost",
        port=8000,
        log_level="info",
        reload=True
    )