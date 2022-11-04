# logging setup
import importlib
import os

from loguru import logger

from components.data.ohlcv import OHLCV
from components.strategy.strategy import Strategy


# import all strategies from STRATEGY_PATH
def import_strategies(strategy_path: str):
    logger.debug('Importing strategies...')
    for file in os.listdir(strategy_path):
        if file.endswith('.py'):
            logger.debug(f'Importing Strategy from: {file}')
            module = importlib.import_module(f'{strategy_path.replace("/", ".")}.{file[:-3]}')
            for name, obj in module.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, Strategy) and obj is not Strategy:
                    logger.debug(f'Imported {obj}')
                    obj()


def import_datasets(dataset_path: str):
    logger.debug('Importing datasets...')
    for file in os.listdir(dataset_path):
        if file.endswith('.csv'):
            logger.debug(f'Importing Dataset from: {file}')
            logger.debug(f'Creating OHLCV from: {file}')
            OHLCV().from_csv(f'{dataset_path}/{file}')


def import_datasets_from_external_source(url: str):
    pass
