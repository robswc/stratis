from typing import Optional, Union

from fastapi import APIRouter
from loguru import logger
from pydantic import BaseModel

from components.ohlc import DataAdapter, CSVAdapter

router = APIRouter()


class DataRequest(BaseModel):
    start: Union[int, None]
    end: Union[int, None]
    kwargs: dict

    class Config:
        schema_extra = {
            "example": {
                "start": None,
                "end": None,
                "kwargs": {
                    "path": "data/AAPL.csv"
                }
            }
        }


@router.post("/{adapter}")
async def get_data(adapter: str, request: DataRequest):
    """Get data from an adapter
    May eventually be a "GET" request, see: https://github.com/swagger-api/swagger-ui/issues/2136
    """
    a = DataAdapter.objects.get(adapter)
    logger.debug(f'Data Endpoint: Using {a.name}')
    logger.debug(f'Data Endpoint: start:{request.start} end:{request.end} kwargs:{request.kwargs}')
    data = a.get_data(request.start, request.end, **request.kwargs)
    return data.to_dict()


@router.get("/adapters", tags=["adapter"])
async def get_adapters():
    """List all data adapters"""
    return [a.name for a in DataAdapter.objects.all()]
