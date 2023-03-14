from fastapi import FastAPI

from api.api_v1.api import api_router
from utils.loaders import load_all  # noqa: F401

app = FastAPI(
    title="Stratis API",
)

app.include_router(api_router, prefix="/api/v1")