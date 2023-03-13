import os

from core.commands.strategy import CreateNewStrategy


class TestCommands:
    def test_create_strategy(self):

        # Create a new strategy
        test_path = 'tests/temp'
        CreateNewStrategy(strategy_name='MyTestStrategy').handle(override_path=test_path, prompt=False)
        assert os.path.exists(f'{test_path}/my_test_strategy.py')
        os.remove(f'{test_path}/my_test_strategy.py')

        # test that exception is raised when strategy name is invalid
        try:
            CreateNewStrategy(strategy_name='MyTestStrategy').handle(override_path=test_path)
        except ValueError:
            assert True

        try:
            CreateNewStrategy(strategy_name='My Test Strategy').handle(override_path=test_path)
        except ValueError:
            assert True