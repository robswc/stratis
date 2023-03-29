from components import Parameter
from components import Strategy, on_step
from components.orders.order import Order
from components.strategy import ta
from components.strategy.decorators import after
from components.strategy.strategy import Plot


class UsingBuiltins(Strategy):
    sma_fast_length = Parameter(10)
    sma_slow_length = Parameter(60)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_close = self.data.all('close')
        if len(self.data) > 0:
            self.sma_faster = ta.sma(all_close, int(self.sma_fast_length) - 5)
            self.sma_fast = ta.sma(all_close, int(self.sma_fast_length))
            self.sma_slow = ta.sma(all_close, int(self.sma_slow_length))
            self.sma_slower = ta.sma(all_close, int(self.sma_slow_length) + 10)
            self.atr = ta.atr(self.data.all('high'), self.data.all('low'), all_close, 14)
            self.kf_1 = ta.kalman_filter(all_close, 600)
            self.kf_2 = ta.kalman_filter(all_close, 600)
            self.kf_3 = ta.kalman_filter(all_close, 600)
            self.kf_4 = ta.kalman_filter(all_close, 400)
            self.kf_5 = ta.kalman_filter(all_close, 500)
            self.kf_6 = ta.kalman_filter(all_close, 600)
            self.kf_7 = ta.kalman_filter(all_close, 700)
            self.correlation = ta.correlation_coefficient(self.sma_fast, self.sma_slow, 14)

    @on_step
    def check_for_crossover(self):
        # add logic to crossover here
        cross_over = ta.logic.crossover(self.sma_fast, self.sma_slow)
        cross_under = ta.logic.crossunder(self.sma_fast, self.sma_slow)
        corr = self.correlation > 0.5
        if cross_over:
            # self.orders.market_order(side='buy', quantity=1)
            self.positions.open(order_type='market', side='buy', quantity=1)
        elif cross_under:
            # self.orders.market_order(side='sell', quantity=1)
            self.positions.close()

    @after
    def create_plots(self):
        self.export_plots([
            Plot(self.sma_fast, name='sma_fast'),
            Plot(self.sma_slow, name='sma_slow'),
        ])

