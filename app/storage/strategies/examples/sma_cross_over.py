from components import Parameter
from components import Strategy, on_step
from components.strategy import ta


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
        pass
