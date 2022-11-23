from components.data.ohlcv import OHLCV
from components.strategy.strategy import Strategy, before, runner, after
from components.strategy import ta


class SMAStrategy(Strategy):
    data = OHLCV().from_csv('storage/data/ohlcv/AAPL.csv')

    sma_slow = []
    sma_fast = []

    @before
    def set_sma(self):
        close_data = self.data.close(as_list=True)
        self.sma_fast = ta.sma(close_data, 10)
        self.sma_slow = ta.sma(close_data, 20)
        self.sma_fast.round(2)
        self.sma_slow.round(2)
        self.sma_slow.replace_none(0)
        self.sma_fast.replace_none(0)

    @runner
    def run(self, parameters):
        idx = self.get_idx()
        if self.sma_fast[idx] > self.sma_slow[idx] and self.sma_fast[idx - 1] < self.sma_slow[idx - 1]:
            self.create_basic_position(
                side='buy',
                quantity=1,
                order_type='MARKET',
                take_profit=self.data.close() + 5,
                take_loss=self.data.close() - 5
            )

    @after
    def run_backtest(self):
        self.backtest.run()
