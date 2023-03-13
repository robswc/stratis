"""
A command-line utility for managing the app.
"""
from core.commands import strategy

import typer

app = typer.Typer()

app.add_typer(strategy.app, name='strategy')

if __name__ == '__main__':
    app()