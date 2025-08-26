import logging

from typer import Typer

from isaac_ase.cli.utils.logging_config import setup_logging
from isaac_ase.play.play_task import PlayTask

app = Typer(add_completion=False)

setup_logging(level="INFO")

logger = logging.getLogger(__name__)


@app.command()
def play():
    play_task = PlayTask()
    play_task.run()


if __name__ == "__main__":
    app()