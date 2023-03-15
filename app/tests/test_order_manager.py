from components.ohlc import OHLC, CSVAdapter
from components.ohlc.symbol import Symbol
from components.orders.order_manager import OrderManager
from components.strategy.strategy import BaseStrategy
from storage.strategies.examples.sma_cross_over import SMACrossOver

STRATEGY = SMACrossOver(
    data=CSVAdapter().get_data('tests/data/AAPL.csv', 'AAPL')
)

class TestOrderManager:
    def test_market_order(self):
        om = OrderManager(STRATEGY)
        om.market_order(side='buy', quantity=1)
        om.show()
