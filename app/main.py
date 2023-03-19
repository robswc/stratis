from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.api_v1.api import api_router
from utils.loaders import load_all  # noqa: F401

app = FastAPI(
    title="Stratis API",
)

allowed_origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

# handle CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")