from components import Parameter
from components import Strategy, on_step
from components.orders.order import Order
from components.strategy import ta
from components.strategy.decorators import after


class SMACrossOver(Strategy):
    sma_fast_length = Parameter(10)
    sma_slow_length = Parameter(60)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_close = self.data.all('close')
        self.sma_fast = ta.sma(all_close, int(self.sma_fast_length))
        self.sma_slow = ta.sma(all_close, int(self.sma_slow_length))

    @on_step
    def check_for_crossover(self):
        # add logic to crossover here
        cross = ta.logic.crossover(self.sma_fast, self.sma_slow)
        if cross:
            self.orders.market_order(side='buy', quantity=1)

    @after
    def print_orders(self):
        print(self.orders.summary())
        self.orders.show()

