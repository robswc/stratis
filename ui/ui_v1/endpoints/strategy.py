from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from components.data.ohlcv import OHLCVManager
from components.strategy.strategy import StrategyManager

router = APIRouter()

templates = Jinja2Templates(directory="templates")

sm = StrategyManager()


@router.get("/")
async def view_all_strategies(request: Request):
    strategies = []
    # request all strategies from strategy manager
    for strategy in sm.strategies:
        strategies.append({'name': strategy.name, 'link': f'/ui/v1/strategy/{strategy.name}'})

    return templates.TemplateResponse(
        name="strategy/view_all.html",
        context={
            "request": request,
            'strategies': strategies
        }
    )


@router.get("/{strategy_name}")
async def view_strategy(request: Request, strategy_name: str):
    strategy = sm.get_strategy(strategy_name)

    dm = OHLCVManager()

    # load datasets
    datasets = dm.datasets

    return templates.TemplateResponse(
        name="strategy/view_strategy.html",
        context={
            "request": request,
            'strategy': strategy,
            'datasets': [{'name': dataset.name, 'id': idx} for idx, dataset in enumerate(datasets)]
        }
    )
