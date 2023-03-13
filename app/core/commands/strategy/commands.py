import os
import string

from components.strategy import Strategy
from core.commands.command import BaseCommand
from utils.commons import STRATEGY_TEMPLATE_PATH
from utils.create_file import create_file
from utils.formatting import snake_case, pascal_case, pascal_to_snake_case
from utils.wiki_link import wiki_link
from rich import print


class CreateNewStrategy(BaseCommand):
    """Creates a new strategy."""

    help = (
        "The name of the strategy, in pascal case, to strategy. (ThisIsPascalCase)  "
        "This will be converted to snake_case and used as the filename.  "
        "Example: 'MyStrategy' will be converted to 'my_strategy.py'."
    )

    template_path = STRATEGY_TEMPLATE_PATH

    strategy_name: str

    def _validate_strategy_name(self):

        validations = [
            self.strategy_name.isidentifier(),
            pascal_case(self.strategy_name).isidentifier(),
            pascal_to_snake_case(self.strategy_name).isidentifier(),
        ]

        if all(validations):
            return True
        msg = (
            f'Invalid strategy name: {self.strategy_name}. '
            f'Strategy names must valid. {wiki_link("https://github.com/robswc/stratis/wiki/Strategies#naming")}'
        )
        raise ValueError(msg)

    def __init__(self, strategy_name: str):
        super().__init__()
        self.strategy_name = strategy_name
        self._validate_strategy_name()

    def handle(self, *args, **kwargs):
        if kwargs.get('override_path'):
            strategy_path = f'{kwargs.get("override_path")}/{pascal_to_snake_case(self.strategy_name)}.py'
        else:
            strategy_path = f'storage/strategies/{pascal_to_snake_case(self.strategy_name)}.py'

        # Open the template file and read its contents
        with open(self.template_path, 'r') as template_file:
            template_contents = template_file.read()

        # Replace the class name in the template contents with the provided name
        new_contents = string.Template(template_contents).substitute(
            StrategyName=self.strategy_name
        )

        # strategy the file
        path, created = create_file(strategy_path, new_contents, prompt=kwargs.get('prompt', True))
        if created:
            print(f'[bold green]Created new strategy at:[/bold green] {path}')
        else:
            print(f'[bold red]Strategy Not Created[/bold red]')

class ListStrategies(BaseCommand):

    help = (
        "Lists all registered strategies"
    )

    def handle(self, *args, **kwargs):
        return [s.name for s in Strategy.objects.all()]