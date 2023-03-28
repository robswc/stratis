from components.backtest.backtest import Backtest
from components.ohlc import CSVAdapter
from storage.strategies.examples.sma_cross_over import SMACrossOver


class TestPositions:
    def test_large_amount_of_positions(self):
        OHLC = CSVAdapter().get_data(start=None, end=None, path='tests/data/AAPL.csv', symbol='AAPL')
        strategy = SMACrossOver(data=OHLC)
        strategy.data.advance_index(100)

        # create positions
        for i in range(500):
            strategy.data.advance_index(5)
            strategy.positions.open(order_type='market', side='buy', quantity=1)
            strategy.data.advance_index(2)
            strategy.positions.close()

        # create backtest
        backtest = Backtest(strategy=strategy, data=OHLC)
        backtest.test()

        # check overview
        print(backtest.result.get_overview())

        assert backtest.result.get_overview().get('trades') == 500