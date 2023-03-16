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

    def test_order_validation(self):
        # valid orders
        Order(
            symbol='BTCUSDT',
            side=Side.BUY,
            type=OrderType.MARKET,
            timestamp=TIMESTAMP,
            qty=1,
        )

        # pytest, test several invalid orders to ensure they all raise a ValidationError
        invalid_orders = [
            # missing symbol
            {"side": Side.BUY, "type": OrderType.MARKET, "timestamp": TIMESTAMP, "qty": 1},
            # missing side
            {"symbol": "BTCUSDT", "type": OrderType.MARKET, "timestamp": TIMESTAMP, "qty": 1},
            # missing type
            {"symbol": "BTCUSDT", "side": Side.BUY, "timestamp": TIMESTAMP, "qty": 1},
            # missing timestamp
            {"symbol": "BTCUSDT", "side": Side.BUY, "type": OrderType.MARKET, "qty": 1},
            # missing qty
            {"symbol": "BTCUSDT", "side": Side.BUY, "type": OrderType.MARKET, "timestamp": TIMESTAMP},
        ]

        for data in invalid_orders:
            with pytest.raises(ValidationError):
                Order(**data)


