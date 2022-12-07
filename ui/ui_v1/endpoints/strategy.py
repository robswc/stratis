from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from components.data.ohlcv import OHLCVManager, OHLCV
from components.strategy.strategy import StrategyManager

router = APIRouter()

templates = Jinja2Templates(directory="templates")

sm = StrategyManager()


@router.get("/", include_in_schema=False)
async def view_all_strategies(request: Request):
    strategies = []
    # request all strategies from strategy manager
    for strategy in sm.strategies:
        strategies.append({'name': strategy.__name__, 'link': f'/ui/v1/strategy/{strategy.__name__}'})

    return templates.TemplateResponse(
        name="strategy/view_all.html",
        context={
            "request": request,
            'strategies': strategies
        }
    )


@router.get("/{strategy_name}", include_in_schema=False)
async def view_strategy(request: Request, strategy_name: str, dataset: str = None):
    strategy = sm.get_new_strategy(strategy_name)
    print('STRATEGY ->', id(strategy))
    if dataset:
        ohlcv = OHLCV().from_api(dataset)
        strategy.data = ohlcv
        strategy.run({})

    dm = OHLCVManager()

    # load datasets
    datasets = dm.datasets

    return templates.TemplateResponse(
        name="strategy/view_strategy.html",
        context={
            "request": request,
            'strategy': strategy,
            'positions': [p.as_json() for p in strategy.backtest.positions],
            'datasets': [{'name': dataset.name, 'id': idx} for idx, dataset in enumerate(datasets)]
        }
    )
