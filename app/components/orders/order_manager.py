from components.orders.order import Order


class OrderManager:
    def __init__(self, strategy):
        self.orders = []
        self.strategy = strategy
        self.symbol = strategy.symbol
        if strategy is None:
            raise ValueError('Strategy is required')


    def market_order(self, side: str, quantity: int):
        order = Order(
            type='market',
            side=side,
            qty=quantity,
            symbol=self.symbol.symbol,
            filled_avg_price=self.strategy.data.close,
            timestamp=self.strategy.data.timestamp,
        )
        self.orders.append(order)
        return order

    def add(self, order: Order):
        self.orders.append(order)

    def all(self):
        return self.orders

    def filter(self, **kwargs):
        return [o for o in self.orders if all([o.__getattribute__(k) == v for k, v in kwargs.items()])]

    def __len__(self):
        return len(self.orders)

    def summary(self):
        return {
            'total': len(self.orders),
        }

    def show(self):
        print('showing orders for strategy: {}'.format(self.strategy.name))
        print('\n'.join([str(o) for o in self.orders]))