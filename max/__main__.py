"""Demonstrate the capabilities of the max package."""
from lorem_text import lorem
from rich import print
from rich.layout import Layout
from rich.panel import Panel
from rich.syntax import Syntax

from max.console import MaxConsole
from max.gradient import Gradient
from max.rule import GradientRule

console = MaxConsole()
console.line(2)

# Random Gradient
console.rule(title="Random Gradient", style="bold.white")
console.line()
syntax_lines = [
    "from lorem_text import lorem\n",
    "from max.gradient import Gradient",
    "from max.console import MaxConsole\n",
    "console = MaxConsole()",
    "TEXT1 = lorem.paragraphs(3)\n",
    "console.print(Gradient(TEXT1), justify='center')",
]
SYNTAX1 = "\n".join(syntax_lines)
console.print(Syntax(SYNTAX1, "python", padding=(1, 2)), justify="center")
console.line()
console.print(
    "[dim]To create a random gradient he only required argument is the text. The \
above code produces the following output:[/]",
    justify="center",
)
console.line()
console.print(Gradient(lorem.paragraphs(3)), justify="center")
console.line(2)

# Specified Gradient
TEXT2 = lorem.paragraphs(3)
console.rule(
    title="[bold white]Gradient <[/][bold.red]Red[/][bold.white] to \
[/][bold.blue]Light_Blue[/][bold.white]>[/]",
    style="bold.white",
)
console.line()
console.print(  # explanation
    "[dim]Specifying a starting color and an ending color allows you to \
specify the colors in the gradient.[/]",
    justify="center",
)
console.line()
syntax_lines = [
    "console.print(",
    "\tGradient(",
    "\t\ttext=lorem.paragraphs(3), start='red', end='light_blue'",
    "\t)",
    ")",
]
SYNTAX2 = Syntax("\n".join(syntax_lines), "python", padding=(1, 2), code_width=70)
console.print(SYNTAX2, justify="center")
console.line()

gradient2 = Gradient(TEXT2, justify="center", start="red", end="light_blue")
console.print(gradient2, justify="left")
console.line(2)

TITLE3 = "[underline bold.white]Inverted Italicized Bold Gradient <[/]"
TITLE3 = f"{TITLE3}[bold.yellow]Yellow[/][bold.white] to[/]"
TITLE3 = f"{TITLE3}[bold.blue]Blue[/][bold.white]>[/]"
TEXT3 = lorem.paragraphs(3)
console.rule(
    title=TITLE3,
    style="bold.white",
)
gradient3 = Gradient(
    TEXT3,
    justify="center",
    start="yellow",
    end="blue",
    invert=True,
    style="italic bold",
)
console.print(gradient3, justify="center")
console.line(2)

console.rule(
    title="[bold.white]Bold Rainbow Gradient(Right Justified)[/]",
    style="bold.white",
)
console.print(Gradient(text=TEXT3, rainbow=True, bold=True), justify="right")
