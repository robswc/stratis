from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from components.data.ohlcv import OHLCVManager
from components.strategy.strategy import StrategyManager

router = APIRouter()

templates = Jinja2Templates(directory="templates")

dm = OHLCVManager()


@router.get("/")
async def view_all_datasets(request: Request):
    datasets = []
    # request all strategies from strategy manager
    for dataset in dm.datasets:
        datasets.append({'name': dataset.name, 'link': f'/ui/v1/strategy/{dataset.name}'})

    return templates.TemplateResponse(
        name="data/view_all_data.html",
        context={
            "request": request,
            'datasets': datasets
        }
    )


@router.get("/{strategy_name}")
async def view_strategy(request: Request, strategy_name: str):
    strategy = sm.get_strategy(strategy_name)
    return templates.TemplateResponse(
        name="strategy/view_strategy.html",
        context={
            "request": request,
            'strategy': strategy
        }
    )
