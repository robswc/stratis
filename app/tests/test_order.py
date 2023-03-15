from datetime import datetime

import pytest
from pydantic import ValidationError

from components.orders.order import Order, OrderSide as Side, OrderType

TIMESTAMP = int(datetime.now().timestamp())

class TestOrders:


    def test_hashing(self):
        fake_order_1 = Order(
            symbol='BTCUSDT',
            side=Side.BUY,
            type=OrderType.MARKET,
            qty=1,
            timestamp=TIMESTAMP,
        )
        fake_order_2 = Order(
            symbol='BTCUSDT',
            side=Side.BUY,
            type=OrderType.MARKET,
            qty=1,
            timestamp=TIMESTAMP,
        )
        assert fake_order_1 == fake_order_2

        fake_order_3 = Order(
            symbol='BTCUSDT',
            side=Side.BUY,
            type=OrderType.MARKET,
            qty=2,
            timestamp=TIMESTAMP,
        )

        assert fake_order_1 != fake_order_3

        # test IDs
        assert fake_order_1.get_id() == fake_order_2.get_id()
        assert fake_order_1.get_id() != fake_order_3.get_id()

    def test_order_validation_qty(self):
        # valid orders
        Order(
            symbol='BTCUSDT',
            side=Side.BUY,
            type=OrderType.MARKET,
            timestamp=TIMESTAMP,
            qty=1,
        )

        # invalid orders
        with pytest.raises(ValidationError):
            Order(symbol='BTCUSDT', side=Side.BUY, type=OrderType.MARKET, timestamp=TIMESTAMP, qty=0)

        with pytest.raises(ValidationError):
            Order(symbol='BTCUSDT', side=Side.BUY, type=OrderType.MARKET, timestamp=TIMESTAMP, qty=None)

        with pytest.raises(ValidationError):
            Order(symbol='BTCUSDT', side=Side.BUY, type=OrderType.MARKET, timestamp=TIMESTAMP, qty=-1)

    def test_order_validation_side(self):
        # valid order
        Order(symbol='BTCUSDT', side=Side.BUY, type=OrderType.MARKET, timestamp=TIMESTAMP, qty=1)

        with pytest.raises(ValidationError):
            Order(symbol='BTCUSDT', side='invalid', type=OrderType.MARKET, timestamp=TIMESTAMP, qty=1)

    def test_order_validation_type(self):
        # valid order
        Order(symbol='BTCUSDT', side=Side.BUY, type=OrderType.MARKET, timestamp=TIMESTAMP, qty=1)

        with pytest.raises(ValidationError):
            Order(symbol='BTCUSDT', side=Side.BUY, type='invalid', timestamp=TIMESTAMP, qty=1)