import random
from typing import Optional, List

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
    cost_basis: Optional[float] = None
    average_entry_price: Optional[float] = None
    average_exit_price: Optional[float] = None
    size: Optional[int] = 0
    side: Optional[str] = None
    unrealized_pnl: Optional[float] = None
    pnl: Optional[float] = None
    timestamp: Optional[int] = None

    def _get_effect(self, order: Order):
        print('getting effect...', abs(self.size), abs(self.size + order.qty))
        if abs(self.size) < abs(self.size + order.qty):
            return PositionEffect.ADD
        else:
            return PositionEffect.REDUCE

    def test(self, ohlc: 'OHLC'):
        for o in self.orders:
            print(self.handle_order(o))

    def add_closing_order(self):
        # creates and adds a closing order to the position
        if self.closed:
            raise PositionClosedException('Position is already closed')

        # create order
        order = Order(
            order_type='market',
            side='buy' if self.side == 'sell' else 'sell',
            quantity=self.size,
            symbol=self.orders[0].symbol,
            timestamp=self.timestamp,
        )

        self.orders.append(order)

    def handle_order(self, order):
        effect = self._get_effect(order)

        if effect == PositionEffect.ADD:
            print('order is add')
            # since the position is added, we need to calculate the cost basis
            self.cost_basis += order.price * order.qty
            self.average_entry_price = self.cost_basis / (self.size + order.qty)

        if effect == PositionEffect.REDUCE:
            print('order is reduce')
            # since the position is reduced, we need to calculate the realized pnl
            realized_pnl = (order.price - self.average_entry_price) * (order.qty * -1 if self.size > 0 else order.qty)
            self.pnl += realized_pnl

        self.size += order.qty
        self.closed = self.size == 0  # if size is 0, position is closed


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
