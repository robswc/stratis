from components.ohlc import OHLC, CSVAdapter
from components.ohlc.symbol import Symbol
from components.orders.order import Order
from components.orders.enums import OrderType
from components.orders.order_manager import OrderManager
from components.strategy.strategy import BaseStrategy
from storage.strategies.examples.sma_cross_over import SMACrossOver

STRATEGY = SMACrossOver(
    data=CSVAdapter().get_data('tests/data/AAPL.csv', 'AAPL')
)
CLOSE = STRATEGY.data.close
TIMESTAMP = STRATEGY.data.timestamp
SYMBOL = STRATEGY.data.symbol.symbol

class TestOrderManager:
    def test_market_order(self):
        om = OrderManager(STRATEGY)
        om.market_order(side='buy', quantity=1)
        om.market_order(side='sell', quantity=1)
        assert len(om) == 2

    def test_add(self):
        om = OrderManager(STRATEGY)
        om.add(Order(side='buy', qty=1, symbol=SYMBOL, filled_avg_price=CLOSE, timestamp=TIMESTAMP, type=OrderType.MARKET))
        om.add(Order(side='sell', qty=1, symbol=SYMBOL, filled_avg_price=CLOSE, timestamp=TIMESTAMP, type=OrderType.MARKET))
        assert len(om) == 2

    def test_summary(self):
        om = OrderManager(STRATEGY)
        om.market_order(side='buy', quantity=1)
        om.market_order(side='sell', quantity=1)
        assert om.summary() == {'total': 2}
