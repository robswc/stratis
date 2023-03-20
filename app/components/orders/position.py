import hashlib
import random
from typing import Optional, List, Union

from loguru import logger
from pydantic import BaseModel

from components.orders.order import Order, StopOrder, LimitOrder


class PositionValidationException(Exception):
    pass

class PositionUnbalancedException(Exception):
    pass

class PositionClosedException(Exception):
    pass


class PositionEffect:
    REDUCE = 'reduce'
    ADD = 'add'


class Position(BaseModel):
    id: Optional[str] = None
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

    def __int__(self):
        super().__init__()
        self.id = self._get_id()

    def __str__(self):
        return f'Position: {""} | {self.side} | {self.size} | {self.cost_basis} | {self.pnl}'

    def _get_id(self):
        """Get the id of the position."""
        order_ids = [o.id for o in self.orders]
        return hashlib.md5(str(order_ids).encode()).hexdigest()

    def _get_effect(self, order: Order):
        """Get the effect of an order on a position."""
        if abs(self.size) < abs(self.size + order.qty):
            return PositionEffect.ADD
        else:
            return PositionEffect.REDUCE

    def _get_size(self):
        """Get the size of all orders in the position."""
        return sum([o.qty for o in self.orders])

    def _get_root_side_orders(self):
        """Get the root side orders of the position."""
        return [o for o in self.orders if o.side == self.side]

    def test(self, ohlc: 'OHLC' = None):
        # iterate over all orders, handling each one
        for o in self.orders:
            try:
                self.handle_order(order=o, ohlc=ohlc)
            except PositionClosedException:
                logger.warning(f'Position {self.id} is already closed')

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

    def _handle_tbd_order(self, order: Union[Order, StopOrder, LimitOrder], ohlc: 'OHLC' = None):
        # get the start index of the OHLC data, which is the index of the first order
        start_index = ohlc.index.get_loc(self.orders[0].timestamp)
        df = ohlc.dataframe.iloc[start_index:]
        # loop through the df
        for index, row in df.iterrows():
            # handle stops
            if order.type == 'stop':
                if self.side == 'buy' and row.low <= order.stop_price:
                    order.filled_timestamp = index
                    order.filled_avg_price = order.stop_price
                    break
                if self.side == 'sell' and row.high >= order.stop_price:
                    order.filled_timestamp = index
                    order.filled_avg_price = order.stop_price
                    break
            # handle limits
            if order.type == 'limit':
                if self.side == 'buy' and row.high >= order.limit_price:
                    order.filled_timestamp = index
                    order.filled_avg_price = order.limit_price
                    break
                if self.side == 'sell' and row.low <= order.limit_price:
                    order.filled_timestamp = index
                    order.filled_avg_price = order.limit_price
                    break

        # if the order is still missing a timestamp, it was never filled
        if order.filled_timestamp is None:
            return
        else:
            order.timestamp = order.filled_timestamp

    def handle_order(self, order: Union[Order, StopOrder, LimitOrder], ohlc: 'OHLC' = None):

        # if the position is closed, we can't handle any more orders
        if self.closed:
            raise PositionClosedException('Position is already closed')

        # handle TBD order
        if order.timestamp is None:
            self._handle_tbd_order(order, ohlc)

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
            # check that the position will not change sides
            if self.side == 'buy' and self.size + order.qty < 0:
                raise PositionUnbalancedException('Position will change sides')
            if self.side == 'sell' and self.size + order.qty > 0:
                raise PositionUnbalancedException('Position will change sides')


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

        # if order is missing filled timestamp, set it to the order timestamp
        if order.filled_timestamp is None:
            order.filled_timestamp = order.timestamp


class BracketPosition(Position):
    pass
