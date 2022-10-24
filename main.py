from fastapi import FastAPI

import settings
from api.api_v1.api import api_router
from ui.ui_v1.ui import ui_router

app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "Hello World"}



app.include_router(ui_router, prefix=settings.UI_V1_STR)
app.include_router(api_router, prefix=settings.API_V1_STR)
