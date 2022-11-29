import csv

import requests
from loguru import logger


class OHLCVManager:
    datasets = []

    def get_dataset(self, name) -> 'OHLCV':
        for dataset in self.datasets:
            if dataset.name == name:
                return dataset
        raise ValueError(f'Dataset {name} not found.')

    def delete(self, name):
        """Deletes a dataset by name."""
        for idx, dataset in enumerate(self.datasets):
            if dataset.name == name:
                del self.datasets[idx]
                return True
        return False

    def add_dataset(self, dataset):
        """Adds a dataset to the manager."""
        existing = self.get_dataset(dataset.name)
        if existing is None:
            self.datasets.append(dataset)
        else:
            logger.warning(f'Dataset {dataset.name} already exists, updating dataset.')
            self.datasets.remove(existing)
            del existing
            self.datasets.append(dataset)
            return True

    def get_new_dataset(self, name):
        """Gets a dataset by name."""
        for d in self.datasets:
            if d.__name__ == name:
                return d()
        return None


class OHLCV(list):
    manager = OHLCVManager

    def __init__(self):
        super().__init__()
        self.raw_data = None
        self.validated_data = None
        self._idx = 0
        self.name = None
        self.manager.datasets.append(self)

    def reset(self):
        self._idx = 0

    def get_index(self):
        return self._idx

    def _load(self, data, validate):
        self.raw_data = data

        # ensure data is valid
        if validate:
            self.validate()

        # set validated data if data is valid
        self.validated_data = self.raw_data

        # convert data to float
        for row in self.validated_data:
            for key in row.keys():
                row[key] = float(row[key])
        self.extend(self.validated_data)
        return self

    def from_csv(self, path):
        # read csv
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            csv_data = [row for row in reader]
        f.close()
        self.name = path.split('/')[-1].split('.')[0]
        return self._load(csv_data, True)

    def from_api(self, dataset=None):
        # url = 'http://192.168.0.216:5510/dataset/ohlc'
        url = 'http://127.0.0.1:8010/dataset/ohlc'
        r = requests.get(
            url=url,
            params={
                'dataset': dataset}
        )
        r.raise_for_status()
        data = r.json().get('data')
        self.name = dataset
        return self._load(data, False)

    def validate(self):
        if len(self.raw_data) == 0:
            raise ValueError('No data to validate')

    def open(self, offset=0, as_list=False):
        return self._get_ohlc('open', offset, as_list)

    def high(self, offset=0, as_list=False):
        return self._get_ohlc('high', offset, as_list)

    def low(self, offset=0, as_list=False):
        return self._get_ohlc('low', offset, as_list)

    def close(self, offset=0, as_list=False):
        return self._get_ohlc('close', offset, as_list)

    def datetime(self, offset=0, as_list=False):
        return self._get_ohlc('datetime', offset)

    def _get_ohlc(self, column, offset=0, as_list=False):
        col_map = {
            'open': 0,
            'high': 1,
            'low': 2,
            'close': 3,
            'volume': 4,
            'datetime': 5
        }
        column_int = col_map.get(column)
        if as_list:
            if offset:
                raise ValueError('Offset not supported for as_list=True')
            return [row[column] for row in self.validated_data]
        return self._ohlc()[column_int]

    def next(self):
        self._idx += 1
        return self._ohlc()

    def get_idx(self):
        return self._idx

    def _ohlc(self):
        try:
            ohlc = (
                self.validated_data[self._idx]['open'],
                self.validated_data[self._idx]['high'],
                self.validated_data[self._idx]['low'],
                self.validated_data[self._idx]['close'],
                self.validated_data[self._idx]['volume'],
                self.validated_data[self._idx]['datetime']
            )
            if ohlc:
                ohlc = tuple(map(float, ohlc))
                return ohlc
            else:
                logger.debug(f'No OHLC data at index {self._idx}')
                raise Exception('No OHLC data')
        except IndexError:
            if self._idx == len(self.validated_data):
                logger.debug(f'End of OHLCV data')
            else:
                logger.error(f'Previous: {self.validated_data[self._idx - 1]}')
                logger.error(f'Index out of range: {self._idx}')
                raise IndexError(f'Index error at: {self._idx}')
        except Exception:
            raise
