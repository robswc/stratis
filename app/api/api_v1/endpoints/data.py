import os
from typing import Optional

from fastapi import APIRouter

from components.ohlc import DataAdapter

router = APIRouter()


@router.get("/")
async def get_data(adapter: str, data: str, bars: Optional[int] = None):
    """
    Get data from a data adapter.
    :param bars: bars back
    :param adapter: name of data adapter
    :param data: data to load
    :return: data
    """
    adapter = DataAdapter.objects.get(adapter)
    print('cwd', os.getcwd())
    data = adapter.get_data(data).to_dict()
    if bars is not None:
        data = data[-bars:]
    return data

@router.get("/adapters", tags=["adapter"])
async def get_adapters():
    """List all data adapters"""
    return [a.name for a in DataAdapter.objects.all()]
