import datetime

from components.strategy.signal import Signal
from components.strategy.strategy import Strategy, runner, after


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
                take_profit=self.data.close() + 10,
                take_loss=self.data.close() - 10,
            )
            self.signal_manager.signals.append(s)

    @after
    def run_backtest(self):
        self.backtest.run()
