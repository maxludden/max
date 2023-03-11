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
from max.console import BaseMaxConsole as MaxConsole
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

    indexes: ColorIndex
    colors: list[NamedColor]
    console: MaxConsole
    invert: Optional[bool]
    title: Optional[str | Text]
    _iter_index: int = 0

    def __init__(
        self,
        text: str | Text = "",
        start: Optional[NamedColor | str | int] = None,
        end: Optional[NamedColor | str | int] = None,
        justify: JustifyMethod = DEFAULT_JUSTIFY,
        invert: bool = False,
        length: int = 4,
        console: MaxConsole = MaxConsole(),  # pylint: disable=W0621:redefined-outer-name
        overflow: OverflowMethod = DEFAULT_OVERFLOW,
        title: str = "Gradient",
        bold: bool = False,
        *,
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
        self.start = start
        self.end = end
        self.invert = bool(invert)
        self.length = length
        self.justify = justify
        self.indexes = []
        self.colors = []
        self.title = title
        self.bold = bold
        self.verbose = verbose

        if self.start in NamedColor.colors:
            self.start = NamedColor.colors.index(self.start)
        elif self.start in NamedColor.hex_colors:
            self.start = NamedColor.hex_colors.index(self.start)
        elif isinstance(self.start, NamedColor):
            self.start = NamedColor(self.start).as_index()
        elif isinstance(self.start, int):
            if self.start not in list(range(0, 9)):
                raise ValueError(
                    f"Invalid start index: {self.start}. Must be between 0 and 9."
                )
        elif self.start is None:
            pass
        else:
            raise TypeError(f"Invalid start type: {type(self.start)}")

        if self.end in NamedColor.colors:
            self.end = NamedColor.colors.index(self.end)
        elif self.end in NamedColor.hex_colors:
            self.end = NamedColor.hex_colors.index(self.end)
        elif isinstance(self.end, NamedColor):
            self.end = NamedColor(self.end).as_index()
        elif isinstance(self.end, int):
            if self.end not in list(range(0, 9)):
                raise ValueError(
                    f"Invalid end index: {self.end}. Must be between 0 and 9."
                )
        elif self.end is None:
            pass
        else:
            raise TypeError(f"Invalid end type: {type(self.end)}")

        if self.start is None and self.end is None:
            self.generate_start_end()
        elif self.start is None and self.end:
            self.generate_start()
        elif self.start and self.end is None:
            self.generate_end()
        else:
            self.generate_index()

        for index in self.indexes:
            self.colors.append(NamedColor.colors[index])

    def generate_start_end(self):
        """Generate the start and end when only `length` is provided."""
        self.start = randint(0, 9)
        self.indexes = []
        for index in range(self.length):
            if not self.invert:
                next_index = self.start + index
            else:
                next_index = self.start - index
            if next_index < 0:
                next_index += 10
            if next_index > 9:
                next_index -= 10
            self.indexes.append(next_index)
        self.end = self.indexes[-1]

    def generate_start(self):
        """Generate the start when only `end` is provided."""
        for index in range(self.length):
            if not self.invert:
                next_index = self.end - index
            else:
                next_index = self.end + index
            if index < 0:
                next_index += 10
            if index > 9:
                next_index -= 10
            self.indexes.append(next_index)

    def generate_end(self):
        """Generate the end when only `start` is provided."""
        self.indexes = []
        for index in range(self.length):
            if not self.invert:
                next_index = self.start + index
            else:
                next_index = self.start - index
            if next_index < 0:
                next_index += 10
            if next_index > 9:
                next_index -= 10
            self.indexes.append(next_index)
        self.end = self.indexes[-1]

    def generate_index(self):
        """Generate the index when both `start` and `end` are provided."""
        self.indexes = []
        if not self.invert:
            if self.start < self.end:
                self.length = (self.end + 1) - self.start
            else:
                self.length = (10 - self.start) + self.end + 1
        else:
            if self.start > self.end:
                self.length = (self.start + 1) - self.end
            else:
                self.length = (10 - self.end) + self.start + 1
        for index in range(self.length):
            if not self.invert:
                next_index = self.start + index
            else:
                next_index = self.start - index
            if next_index < 0:
                next_index += 10
            if next_index > 9:
                next_index -= 10
            self.indexes.append(next_index)
        assert next_index == self.end, f"{next_index} != {self.end}"

    def __getitem__(self, index):
        if index >= len(self.indexes):
            raise IndexError("ColorIndex index out of range")
        return self.indexes[index]

    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        if self._iter_index >= len(self.indexes):
            raise StopIteration
        value = self.indexes[self._iter_index]
        self._iter_index += 1
        return value

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
                if not self.bold:
                    substring.stylize(color, x, x + 1)
                else:
                    substring.stylize(f"bold {color}", x, x + 1)

            gradient_text = Text.assemble(
                gradient_text,
                substring,
                justify=self.justify,
                overflow=self.overflow,
                end=self.end,
            )
        return gradient_text


if __name__ == "__main__":
    console = MaxConsole(justify="center")
    register_repr(Gradient)(normal_repr)
    register_repr(ColorIndex)(normal_repr)
    # console.clear()
    console.line(2)

    text1 = lorem.paragraph()
    console.rule(title="Random Gradient", style="bold.white")
    gradient1 = Gradient(text1, title="Gradient <Random>")
    console.print(gradient1, justify="center")
    console.line(2)

    text2 = lorem.paragraph()
    console.rule(
        title="[bold white]Gradient <[/][bold.red]Red[/][bold.white] to \
[/][bold.blue]Light_Blue[/][bold.white]>[/]",
        style="bold.white",
    )
    gradient2 = Gradient(text2, justify="center", start="red", end="light_blue")
    console.print(gradient2, width=115, justify="center")
    console.line(2)

    text3 = lorem.paragraph()
    console.rule(
        title="[bold.white]Bold Inverted Gradient <[/][bold.yellow]Yellow[/][bold.white] to \
[/][bold.blue]Blue[/][bold.white]>[/]",
        style="bold.white",
    )
    gradient3 = Gradient(
        text3, justify="center", start="yellow", end="blue", invert=True, bold=True
    )
    console.print(gradient3, justify="center")
    console.line(2)
