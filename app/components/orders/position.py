import random
from typing import Optional, List

from loguru import logger
from pydantic import BaseModel

from components.orders.order import Order


class PositionValidationException(Exception):
    pass


class PositionClosedException(Exception):
    pass


class PositionEffect:
    REDUCE = 'reduce'
    ADD = 'add'


class Position(BaseModel):
    orders: List[Order] = []
    closed: bool = False
    cost_basis: Optional[float] = 0
    average_entry_price: Optional[float] = None
    average_exit_price: Optional[float] = None
    size: Optional[int] = 0
    largest_size: Optional[int] = 0
    side: Optional[str] = None
    unrealized_pnl: Optional[float] = None
    pnl: Optional[float] = 0
    opened_timestamp: Optional[int] = None
    closed_timestamp: Optional[int] = None

    def _get_effect(self, order: Order):
        """Get the effect of an order on a position."""
        print(self.size, self.size + order.qty)
        if abs(self.size) < abs(self.size + order.qty):
            return PositionEffect.ADD
        else:
            return PositionEffect.REDUCE

    def _get_size(self):
        """Get the size of all orders in the position."""
        return sum([o.qty for o in self.orders])

    def test(self, ohlc: 'OHLC' = None):
        # iterate over all orders, handling each one
        for o in self.orders:
            self.handle_order(o)

    def add_closing_order(self, ohlc: 'OHLC'):
        """Adds a calculated closing order to the position."""
        if self.closed:
            raise PositionClosedException('Position is already closed')

        # create the closing order
        order = Order(
            type='market',
            side='buy' if self.side == 'sell' else 'sell',
            qty=self._get_size() * -1,
            symbol=self.orders[0].symbol,
            filled_avg_price=ohlc.close,
            timestamp=ohlc.timestamp,
        )

        self.orders.append(order)

    def handle_order(self, order: Order):

        if order.type == 'stop':
            logger.warning('Stop orders are not yet supported!')
            return

        # if the position is missing a side, set it to the side of the first order
        if self.side is None:
            self.side = order.side

        # gets the position effect, either add or reduce
        effect = self._get_effect(order)

        if effect == PositionEffect.ADD:
            # since the position is added, we need to calculate the cost basis
            self.cost_basis += order.filled_avg_price * order.qty
            # adjust the average entry price
            self.average_entry_price = self.cost_basis / (self.size + order.qty)

        if effect == PositionEffect.REDUCE:
            # if the position is closed, set the closed timestamp
            self.closed_timestamp = order.timestamp
            # since the position is reduced, we need to calculate the realized pnl
            realized_pnl = (order.filled_avg_price - self.average_entry_price) * (order.qty * -1 if self.size > 0 else order.qty)
            # adjust the average exit price
            self.average_exit_price = ((self.average_exit_price + order.filled_avg_price) / 2) if self.average_exit_price else order.filled_avg_price
            self.pnl += realized_pnl

        # adjust the size, if the size is 0, the position is closed
        self.size += order.qty
        self.largest_size = self.size if abs(self.size) > abs(self.largest_size) else self.largest_size
        self.opened_timestamp = order.timestamp if self.opened_timestamp is None else self.opened_timestamp
        self.closed = self.size == 0


class BracketPosition(BaseModel):
    take_profit: Optional[Order]
    stop_loss: Optional[Order]

    # def validate(self, **kwargs):
    #     super().validate(**kwargs)
    #     # ensure that both take_profit and stop_loss are not None
    #     if self.take_profit is None and self.stop_loss is None:
    #         raise PositionValidationException('Both take_profit and stop_loss cannot be None.')
    #     # ensure that all orders are of the same symbol
    #     if self.take_profit.symbol != self.stop_loss.symbol:
    #         raise PositionValidationException('All orders must be of the same symbol.')
