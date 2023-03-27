import concurrent.futures
from typing import Optional, List, Union

from loguru import logger
from pydantic import BaseModel

from components.backtest.utils import remove_overlapping_positions
from components.orders.order import Order
from components.positions.positions import Position


def get_effect(position: Position, order: Order):
    """Get the effect of an order on a position."""
    if position.get_size() > 0:
        if order.side == 'buy':
            return 'increase'
        elif order.side == 'sell':
            return 'decrease'
    elif position.get_size() < 0:
        if order.side == 'buy':
            return 'decrease'
        elif order.side == 'sell':
            return 'increase'
    else:
        return 'increase'


class BacktestResult(BaseModel):
    pnl: float
    wl_ratio: float
    sharpe_ratio: Optional[float]
    max_drawdown: Optional[float]
    max_drawdown_duration: Optional[int]
    trades: int
    winning_trades: int
    losing_trades: int
    positions: List[Position]
    orders: List[Order]

    def get_overview(self):
        """Get a dict with the most important backtest results."""
        return {
            'pnl': self.pnl,
            'wl_ratio': self.wl_ratio,
            'trades': self.trades,
            'winning_trades': self.winning_trades,
            'losing_trades': self.losing_trades,
        }


class Backtest:
    def __init__(self, data, strategy):
        self.data = data
        self.strategy = strategy
        self.result: Union[BacktestResult, None] = None

    def _get_orders_with_filled_timestamp(self, orders):
        return [o for o in orders if o.filled_timestamp is not None]

    def _sort_orders(self, orders: List[Order]):
        return sorted(orders, key=lambda x: x.timestamp)

    def test(self):
        logger.debug(f'Starting backtest for strategy {self.strategy.name}')

        positions = self.strategy.positions.all()
        orders = self.strategy.orders.all()

        # use concurrent futures to test orders in parallel
        logger.debug(f'Testing {len(positions)} positions in parallel...')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for p in positions:
                executor.submit(p.test, self.data)
        logger.debug(f'Finished testing {len(positions)} positions in parallel.')

        # after all positions have been tested, we can check for overlapping positions
        positions = remove_overlapping_positions(positions, max_overlap=0)

        all_position_orders = []
        for p in positions:
            all_position_orders += p.orders

        # calculate win/loss ratio
        losing_trades = len([p for p in positions if p.pnl < 0])
        winning_trades = len([p for p in positions if p.pnl > 0])
        if losing_trades == 0:
            wl_ratio = 1
        elif winning_trades == 0:
            wl_ratio = 0
        else:
            wl_ratio = round(winning_trades / (winning_trades + losing_trades), 2)

        # filter and sort orders
        result_orders = self._get_orders_with_filled_timestamp(orders + all_position_orders)
        # sort ascending by timestamp
        result_orders = self._sort_orders(result_orders)

        # create backtest result
        self.result = BacktestResult(
            pnl=sum([position.pnl for position in positions]),
            wl_ratio=wl_ratio,
            trades=len(positions),
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            positions=positions,
            orders=result_orders,
        )
