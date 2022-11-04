import datetime

from components.data.ohlcv import OHLCV
from components.strategy.signal import Signal
from components.strategy.strategy import Strategy, before, runner, after, Parameter
from components.strategy import ta


class BuySignalEvery15Min(Strategy):

    @runner
    def run(self, parameters):
        idx = self.get_idx()
        ts = datetime.datetime.fromtimestamp(self.data.datetime() / 1000)
        if ts.minute % 15 == 0:
            s = Signal(
                timestamp=int(ts.timestamp()),
                side='buy',
                price=self.data.close(),
            )
            self.signal_manager.signals.append(s)


    @after
    def run_backtest(self):
        self.backtest.run()
