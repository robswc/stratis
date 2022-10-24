import importlib
from components.strategy.strategy import Strategy
import os
from loguru import logger

from utils import import_strategies, import_datasets

UI_V1_STR = '/ui/v1'
API_V1_STR = '/api/v1'

# handle strategies
STRATEGY_PATH = 'storage/strategies'
DATASET_PATH = 'storage/data/ohlcv'

import_strategies(STRATEGY_PATH)
import_datasets(DATASET_PATH)
