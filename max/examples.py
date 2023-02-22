"""
Demonstrates a Rich "application" using the Layout and Live classes.

"""
# pylint: disable=unused-import
from datetime import datetime
from random import randint
from time import sleep

from rich.panel import Panel
from rich.text import Text

from max.console import MaxConsole

def _colorful_console() -> Text:
    """Print out `MaxConsole` in a gradient"""
    letters = [
        Text("M", style="bold.green"),
        Text("a", style="bold.yellow"),
        Text("x", style="bold.orange"),
        Text("C", style="bold.red"),
        Text("o", style="bold.magenta"),
        Text("n", style="bold.light_purple"),
        Text("s", style="bold.purple"),
        Text("o", style="bold.blue"),
        Text("l", style="bold.light_blue"),
        Text("e", style="bold.cyan"),
    ]
    # console.log(Text.assemble(*letters))
    return Text.assemble(*letters)


def gen_explanation() -> Text:
    """Generate an explanation of MaxConsole for demonstration."""
    colorful = _colorful_console()
    explanation_text = Text.from_markup(
        " is a custom themed class inheriting from \
[bold #00ffff]rich.console.Console[/]. It is a [italic #b219ff]global singleton \
[/]class that can be imported and used anywhere in the project and \
used as a drop in replacement for [bold #00ffff]rich.console.Console[/].\n\n"
    )
    combine_explanation = Text.assemble("\n\n", colorful, explanation_text)
    return combine_explanation


if __name__ == "__main__":
    console = MaxConsole()
    explanation = gen_explanation()
    title = _colorful_console()
    console.line(2)
    console.print(
        Panel(
            explanation,
            title=title,
            padding=(1, 8),
            width=100,
        ),
        justify="center",
    )
    console.line()
