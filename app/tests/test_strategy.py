from components.strategy import Strategy


class TestStrategy:
    def test_strategy_name(self):
        assert Strategy().name == 'Strategy'
