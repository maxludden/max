"""This module contains the gradient class to automate the creation of gradient colored text."""
# pylint: disable=W0612:unused-variable
# pylint: disable=R0913:too-many-arguments
# pylint: disable=C0103:invalid-name
from random import randint
from typing import Optional

from cheap_repr import normal_repr, register_repr
from lorem_text import lorem
from rich.console import JustifyMethod, OverflowMethod, RenderResult
from rich.control import strip_control_codes
from rich.text import Text

from max.color_index import ColorIndex
from max.console import MaxConsole
from max.log import log
from max.named_color import NamedColor

DEFAULT_JUSTIFY: "JustifyMethod" = "default"
DEFAULT_OVERFLOW: "OverflowMethod" = "fold"


class Gradient(Text):
    """Print gradient colored text to the console.
        Args:
            console(`MaxConsole`): The rich console to print \
                gradient text to. Defaults to MaxConsole().
            text(`text): The text to print. Defaults to empty string.
            start(`NamedColor | str | int`): The color to start the gradient.
            end(`NamedColor|str|int`): The color to end the gradient.
            invert(`bool): Reverse the color gradient. Defaults to False.
            length(`int`): The number of colors in the gradient. Defaults to `3`.
            justify(`JustifyMethod`): How to align the gradient text locally. Defaults \
                to `left`.
            title(`str|Text'): The optional title of the Gradient. Defaults to 'Gradient'
    """

    start_index: int
    end_index: int
    indexes: ColorIndex
    colors: list[NamedColor]
    console: MaxConsole
    _start: Optional[NamedColor | str | int]
    _end: Optional[NamedColor | str | int]
    invert: Optional[bool]
    title: Optional[str | Text]

    def __init__(
        self,
        text: str | Text = "",
        start: Optional[NamedColor | str | int] = None,
        end: Optional[NamedColor | str | int] = None,
        justify: JustifyMethod = DEFAULT_JUSTIFY,
        invert: bool = False,
        length: int = 3,
        console: MaxConsole = MaxConsole(),  # pylint: disable=W0621:redefined-outer-name
        overflow: OverflowMethod = DEFAULT_OVERFLOW,
        title: str = "Gradient",
        verbose: bool = False,
    ) -> None:
        """Print gradient colored text to the console.
        Args:
            text(`text): The text to print. Defaults to empty string.
            start(`Optional[NamedColor|str|int]`): The color to start the gradient.
            end(`Optional[NamedColor|str|int]`): The color to end the gradient.
            justify(`JustifyMethod`): How to align the gradient text locally. Defaults \
                to `left`.
            invert(`bool): Reverse the color gradient. Defaults to False.
            length(`int`): The number of colors in the gradient. Defaults to `3`.
            console(`MaxConsole`): The rich console to print \
                gradient text to. Defaults to MaxConsole().
            title(`str|Text'): The optional title of the Gradient. Defaults to 'Gradient'
        """
        if isinstance(text, Text):
            text = str(text)
        super().__init__(text=text, justify=justify, overflow=overflow)
        self.console = console
        self.text = strip_control_codes(text)
        self.start = NamedColor(start)
        self.end = NamedColor(end)
        self.invert = bool(invert)
        self.length = length
        self.justify = justify
        self.indexes = []
        self.colors = []
        self.title = title

        if self.start is None and self.end is None:
            start_index = randint(0, 9)
            self.start = NamedColor(start_index)
            if self.invert:
                end_index = start_index - int(self.length)
            else:
                end_index = start_index + int(self.length)
            self.end = NamedColor(end_index)
            if verbose:
                log.debug(f"None-none: random start_index: {self.start.as_index()}")
                log.debug(f"None-none: random end_index: {self.end.as_index()}")

        elif self.end is None and self.start:
            if self.invert:
                end_index = self.start.as_index() + int(self.length)
            else:
                end_index = self.start.as_index() - int(self.length)
            self.end = NamedColor(end_index)
            if verbose:
                log.debug(f"start-none: random start_index: {self.start.value}")
                log.debug(f"start-none: random end_index: {self.end.as_index()}")

        elif self.start is None and self.end:
            if self.invert:
                start_index = self.end.as_index() - int(self.length)
            else:
                start_index = self.end.as_index() + int(self.length)
            self.start = NamedColor(start_index)
            if verbose:
                log.debug(f"None-end: random start_index: {self.start.as_index()}")
                log.debug(f"None-end: random end_index: {self.end.value}")

        else:
            if verbose:
                log.debug(f"start: {self.start.value}\nend: {self.end.value}\n")

        self.indexes = ColorIndex(
            start=self.start.as_index(),
            end=self.end.as_index(),
            invert=self.invert,
            length=self.length,
            title=self.title,
        )
        self.length = len(self.indexes)
        if verbose:
            log.debug(f"Indexes: {self.indexes}")
        for index in self.indexes:
            self.colors.append(NamedColor(index))

    def __str__(self):
        return self.text

    def __repr__(self) -> str:
        return f"Gradient<{', '.join([str(color) for color in self.colors])}>, Text<{self.text}>"

    def __rich__(self) -> RenderResult:
        """Rich representation of a gradient object."""
        size = len(self.text)
        gradient_size = size // (self.length - 1)
        gradient_text = Text()

        for index in range(self.length - 1):
            next_index = index + 1
            begin = index * gradient_size
            end = begin + gradient_size
            substring = Text(self.text[begin:end])

            if index < (self.length - 1):
                color1 = self.colors[index]
                r1, g1, b1 = tuple(NamedColor(color1).as_rgb())
                color2 = self.colors[next_index]
                r2, g2, b2 = tuple(NamedColor(color2).as_rgb())
                dr = r2 - r1
                dg = g2 - g1
                db = b2 - b1

            for x in range(gradient_size):
                blend = x / gradient_size
                color = f"#{int(r1 + dr * blend):02X}\
{int(g1 + dg * blend):02X}{int(b1 + db * blend):02X}"
                substring.stylize(color, x, x + 1)

            gradient_text = Text.assemble(
                gradient_text,
                substring,
                justify=self.justify,
                overflow=self.overflow,
                end=self.end,
            )
        return gradient_text


if __name__ == "__main__":
    console = MaxConsole(width=125)
    register_repr(Gradient)(normal_repr)
    register_repr(ColorIndex)(normal_repr)
    console.clear()
    console.line(2)

    text1 = lorem.paragraph()
    console.rule(title="Random Gradient", style="bold.white")
    gradient1 = Gradient(text1, title="Gradient <Random>", verbose=True)
    console.print(gradient1, justify="center")
    console.line(2)

    text2 = lorem.paragraph()
    console.rule(
        title="[bold white]Gradient <[/][bold #ff0000]Red[/][bold white] to \
[/][bold #0000ff]Blue[/][bold white]>[/]",
        style="bold.white",
    )
    gradient2 = Gradient(text2, justify="center", start="red", end="blue")
    console.print(gradient2, justify="center")
    console.line(2)

    text3 = lorem.paragraph()
    console.rule(
        title="[bold white]Inverted Gradient <[/][bold #ff00ff]Magenta[/][bold white] to \
[/][bold #ff0000]Red[/][bold white]>[/]",
        style="bold.white",
    )
    gradient3 = Gradient(
        text3, justify="center", start="magenta", end="red", invert=True
    )
    console.print(gradient3, justify="center")
    console.line(2)
