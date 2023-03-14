class TestDataAdapters:
    def test_init_data_adapter(self):
        from components.ohlc import DataAdapter
        adapter = DataAdapter()
        assert adapter.name == 'DataAdapter'

        # test csv adapter
        from components.ohlc import CSVAdapter
        csv_adapter = CSVAdapter()
        assert csv_adapter.name == 'CSVAdapter'

    def test_csv_adapter(self):
        from components.ohlc import CSVAdapter
        csv_adapter = CSVAdapter()
        ohlc = csv_adapter.get_data('tests/data/AAPL.csv', 'AAPL')
        assert str(ohlc.symbol) == 'AAPL'
        assert ohlc.dataframe.shape == (5001, 5)
