from fastapi import APIRouter
from pydantic import BaseModel

from components.data.ohlcv import OHLCVManager

router = APIRouter()


class DatasetRequest(BaseModel):
    name: str


dm = OHLCVManager()


@router.get("/all")
async def get_all_datasets():
    return [dataset.name for dataset in dm.datasets]


@router.get("")
async def get_dataset(name: str):
    return dm.get_dataset(name)
