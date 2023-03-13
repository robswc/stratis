import typer

from core.commands.strategy.commands import CreateNewStrategy, ListStrategies

app = typer.Typer(
    help="Manage strategies",
)


@app.command()
def create(name: str = typer.Argument(..., help=CreateNewStrategy.help)):
    """
    Create a new strategy
    """
    typer.echo(f"Creating strategy: {name}")
    CreateNewStrategy(strategy_name=name).handle()

@app.command(name="list")
def list_strategies():
    """
    List all strategies
    """
    typer.echo("Listing strategies")
    from utils import strategy_loader  # noqa: F401
    ListStrategies().handle()