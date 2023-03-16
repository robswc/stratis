import random
from typing import Optional, List

from pydantic import BaseModel

from components.orders.order import Order


class PositionValidationException(Exception):
    pass

class PositionClosedException(Exception):
    pass

class Position(BaseModel):
    orders: List[Order] = []
    closed: bool = False
    average_entry_price: Optional[float] = None
    average_exit_price: Optional[float] = None
    size: Optional[int] = None
    side: Optional[str] = None
    pnl: Optional[float] = None
    timestamp: Optional[int] = None

    # TODO: restructure position to be more efficient

    def test(self, ohlc: 'OHLC'):
        self.pnl = self.calc_pnl()

    def add_order(self, order: Order):
        if self.closed:
            raise PositionClosedException('Position is already closed')

        # else we add the order
        self.orders.append(order)

        long_qty = sum([o.qty for o in self.orders if o.side == 'buy'])
        short_qty = sum([o.qty for o in self.orders if o.side == 'sell'])
        self.closed = long_qty == short_qty

    def get_size(self):
        return sum([order.qty for order in self.orders])

    def get_all_buy_orders(self):
        return [order for order in self.orders if order.side == 'buy']

    def get_all_sell_orders(self):
        return [order for order in self.orders if order.side == 'sell']

    def get_average_entry_price(self):
        if self.orders[0].side == 'buy':
            return sum([o.filled_avg_price for o in self.get_all_buy_orders()]) / len(self.get_all_buy_orders())
        else:
            return sum([o.filled_avg_price for o in self.get_all_sell_orders()]) / len(self.get_all_sell_orders())

    def get_average_exit_price(self):
        if self.orders[0].side == 'buy':
            return sum([o.filled_avg_price for o in self.get_all_sell_orders()]) / len(self.get_all_sell_orders())
        else:
            return sum([o.filled_avg_price for o in self.get_all_buy_orders()]) / len(self.get_all_buy_orders())

    def get_side(self):
        return self.orders[0].side

    def get_timestamp(self):
        return self.orders[-1].timestamp

    def calc_pnl(self):
        if self.closed:
            # root order direction
            root_order_side = self.orders[0].side

            # calculate pnl
            if root_order_side == 'buy':
                return (self.get_average_exit_price() - self.get_average_entry_price()) * self.get_size()
            else:
                return (self.get_average_entry_price() - self.get_average_exit_price()) * self.get_size()
        return 0

    def dict(self, **kwargs):
        d = super().dict(**kwargs)
        if self.closed:
            d['average_entry_price'] = self.get_average_entry_price()
            d['average_exit_price'] = self.get_average_exit_price()
            d['size'] = self.get_size() / 2
            d['side'] = self.get_side()
            d['timestamp'] = self.get_timestamp()
            d['pnl'] = self.calc_pnl()
        else:
            d['average_entry_price'] = self.get_average_entry_price()
            d['size'] = self.get_size()
            d['side'] = self.get_side()
            d['timestamp'] = self.get_timestamp()
            d['pnl'] = self.calc_pnl()
        return d


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