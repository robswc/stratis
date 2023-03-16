from components.backtest.backtest import Backtest
from components.ohlc import CSVAdapter
from storage.strategies.examples.sma_cross_over import SMACrossOver

OHLC = CSVAdapter().get_data('tests/data/AAPL.csv', 'AAPL')
STRATEGY = SMACrossOver(data=OHLC)

class TestBacktest:
    def test_backtest_orders(self):

        # add orders
        STRATEGY.orders.market_order(side='buy', quantity=1)

        backtest = Backtest(strategy=STRATEGY, data=OHLC)
        backtest.test()

        assert backtest.result is not None

    def test_backtest_positions(self):

        # add positions
        STRATEGY.positions.open(order_type='market', side='buy', quantity=1)

        backtest = Backtest(strategy=STRATEGY, data=OHLC)
        backtest.test()

        assert backtest.result is not None
