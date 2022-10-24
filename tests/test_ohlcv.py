from components.data.ohlcv import OHLCV


class TestOhlcv:
    def test_load(self):
        assert True

    def test_from_csv(self):
        # test loading valid data
        ohlcv = OHLCV().from_csv('fixtures/ohlc_valid.csv')
        assert len(ohlcv.validated_data) == 5425
        assert len(ohlcv) == 5425

    def test_validate(self):
        assert True

    def test_close(self):
        assert True
