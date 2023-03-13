# dynamically import all strategies in the storage/strategies folder
import inspect
from pathlib import Path
from importlib import import_module
from typing import List, Type
from loguru import logger

from components.strategy.strategy import BaseStrategy

def import_all_strategies() -> List[Type[BaseStrategy]]:
    strategies = []
    # get all paths in the strategies folder, including subfolders, assuming sources root is app/
    paths = Path(__file__).parent.parent.joinpath('storage/strategies').rglob('*.py')
    for path in paths:

        # get the module name from the path
        module_name = path.as_posix().replace('/', '.').replace('.py', '')
        module_name = module_name.split('app.')[1]
        # import the module
        module = import_module(module_name)
        # get all classes in the module
        for name, obj in inspect.getmembers(module):
            # dynamically import all strategies in the storage/strategies folder
            if inspect.isclass(obj) and issubclass(obj, BaseStrategy):
                if obj.__name__ != 'BaseStrategy':
                    strategies.append(obj)
    return strategies

def register_all_strategies():
    strategies = import_all_strategies()
    for strategy in strategies:
        strategy.objects.register(strategy)


loaded_strategies = import_all_strategies()
logger.info(f'Imported {len(loaded_strategies)} strategies')
for s in loaded_strategies:
    logger.info(f'\t->\t{s.__name__} ({s.__module__})')

logger.info('Registering strategies')
register_all_strategies()
logger.info('Strategy loader finished')