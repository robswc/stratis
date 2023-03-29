import hashlib
from typing import Optional, List, Union

import pandas as pd
from loguru import logger
from pydantic import BaseModel

from components.orders.order import Order, StopOrder, LimitOrder
from components.positions.enums import PositionEffect
from components.positions.exceptions import PositionUnbalancedException, PositionClosedException


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
    is_tested: bool = False

    def __int__(self):
        super().__init__()
        self.id = self._get_id()

    def __str__(self):
        return f'Position: {""}\t[{self.side.upper()}]\t{self.size} {self.average_entry_price} -> ' \
               f'{self.average_exit_price} \t pnl:{round(self.pnl, 2)} (opn:' \
               f' {self.opened_timestamp}, cls: {self.closed_timestamp})'

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

    def _get_root_side_orders(self):
        """Get the root side orders of the position."""
        return [o for o in self.orders if o.side == self.side]

    def get_size(self):
        """Get the size of all orders in the position."""
        return sum([o.qty for o in self.orders])

    def get_side(self):
        """Returns the side of the position, either buy or sell."""
        if self.side is None:
            return self.orders[0].side
        return self.side

    def _update_average_entry(self, order: Order):
        if self.average_exit_price:
            self.average_exit_price = ((self.average_exit_price + order.filled_avg_price) / 2)
        else:
            self.average_exit_price = order.filled_avg_price

    def _update_pnl(self, order: Order):
        difference = order.filled_avg_price - self.average_entry_price
        multiplier = -1 if self.get_side() == 'sell' else 1
        realized_pnl = (difference * abs(order.qty)) * multiplier
        self.pnl += realized_pnl

    def _update_largest_size(self):
        if abs(self.size) > self.largest_size:
            self.largest_size = abs(self.size)

    def _update_opened_timestamp(self, order: Order):
        if self.opened_timestamp is None:
            self.opened_timestamp = order.timestamp

    def _add_order_to_size(self, order: Order):
        self.size += order.qty

    def _fill_order(self, order: Union[Order, StopOrder, LimitOrder], ohlc: 'OHLC' = None):
        """Handles TBD orders. Sets the timestamp and fills the order if it was filled."""
        start_index = ohlc.index.get_loc(self.orders[0].timestamp)
        df = ohlc.dataframe.iloc[start_index + 1:]

        if order.type == 'stop':
            filled_order = self._process_stop_order(order, df)
        elif order.type == 'limit':
            filled_order = self._process_limit_order(order, df)

        if filled_order is None:
            self._handle_unfilled_order(order)
        else:
            order.timestamp = order.filled_timestamp

    def _process_stop_order(self, order, df: pd.DataFrame):
        condition = (df.low <= order.stop_price) if self.side == 'buy' else (df.high >= order.stop_price)
        filtered_df = df[condition]

        if not filtered_df.empty:
            filled_row = filtered_df.iloc[0]
            order.filled_timestamp = filled_row.name
            order.filled_avg_price = order.stop_price
            return order
        return None

    def _process_limit_order(self, order, df: pd.DataFrame):
        condition = (df.high >= order.limit_price) if self.side == 'buy' else (df.low <= order.limit_price)
        filtered_df = df[condition]

        if not filtered_df.empty:
            filled_row = filtered_df.iloc[0]
            order.filled_timestamp = filled_row.name
            order.filled_avg_price = order.limit_price
            return order
        return None

    def _handle_unfilled_order(self, order):
        logger.warning(f'Order {order.get_id()} was never filled')
        logger.warning(f'{self}')
        for order in self.orders:
            logger.warning(f'\t{order}')
        # set order did not fill to true
        order.did_not_fill = True
        return

    def handle_order(self, order: Union[Order, StopOrder, LimitOrder], ohlc: 'OHLC' = None):

        # if order isn't already filled, it cannot be handled yet
        if order.filled_timestamp is None:
            return

        # if the position is closed, we can't handle any more orders
        if self.closed:
            raise PositionClosedException('Position is already closed')

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

            # since the position is reduced, we need to re-calculate the average entry price and update the PNL
            self._update_average_entry(order)
            self._update_pnl(order)

        # adjust the size, if the size is 0, the position is closed
        self._add_order_to_size(order)
        self._update_largest_size()
        self._update_opened_timestamp(order)

        # set closed, update closed timestamp if closed
        self.closed = self.size == 0
        if self.closed:
            self.closed_timestamp = order.timestamp

        # if order is missing filled timestamp, set it to the order timestamp
        if order.filled_timestamp is None:
            order.filled_timestamp = order.timestamp

    def test(self, ohlc: 'OHLC' = None):
        """Backtest the position."""
        # handle all orders with a filled timestamp, as these are already filled
        filled_orders = [o for o in self.orders if o.filled_timestamp is not None]
        for order in filled_orders:
            self.handle_order(order=order, ohlc=ohlc)

        # if there are still working orders, handle them
        working_orders = [o for o in self.orders if o.filled_timestamp is None]
        if len(working_orders) > 0:

            # handle all orders without a filled timestamp, as these are TBD
            for order in working_orders:
                self._fill_order(order=order, ohlc=ohlc)

            # determine which order was filled first, filter out any orders that were never filled
            filled_working_orders = [o for o in working_orders if o.filled_timestamp is not None]
            sorted_orders = sorted(filled_working_orders, key=lambda o: o.timestamp)

            # handle the first order
            first_order = sorted_orders[0]
            self.handle_order(order=first_order, ohlc=ohlc)

            # set the remaining order's filled_timestamp to None
            for order in sorted_orders[1:]:
                order.filled_timestamp = None


class BracketPosition(Position):
    def __init__(self):
        super().__init__()
        self.stop_order: Union[StopOrder, None] = None
        self.limit_order: Union[LimitOrder, None] = None
