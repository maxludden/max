"""This module contains the gradient class to automate the creation of gradient colored text."""
# pylint: disable=unused-variable, redefined-outer-name
# pylint: disable=R0913:too-many-arguments
# pylint: disable=C0103:invalid-name

# from concurrent.futures import ThreadPoolExecutor, as_completed
# from multiprocessing import cpu_count
from random import randint
from typing import Optional

from cheap_repr import normal_repr, register_repr
from lorem_text import lorem
from rich.console import ConsoleOptions, JustifyMethod, OverflowMethod, RenderResult
from rich.containers import Lines
from rich.control import strip_control_codes
from rich.style import StyleType
from rich.text import Text

from max.color_index import ColorIndex
from max.console import MaxConsole
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
        overflow: OverflowMethod = DEFAULT_OVERFLOW,
        invert: bool = False,
        length: int = 3,
        console: MaxConsole = MaxConsole(),  # pylint: disable=W0621:redefined-outer-name
        title: str = "Gradient",
        style: StyleType = None,
        bold: bool = False,
        underline: bool = False,
        italic: bool = False,
        rainbow: bool = False,
        string_end: str = "\n",
        *,
        verbose: bool = False,
    ) -> None:
        """Print gradient colored text to the console.
        Args:
            text(`text): The text to print. Defaults to empty string.
            start(`Optional[NamedColor|str|int]`): The color to start the gradient.
            end(`Optional[NamedColor|str|int]`): The color to end the gradient.
            justify(`JustifyMethod`): How to align the gradient text locally. Defaults \
                to `default`.
            overflow(`OverflowMethod`): How to handle text that overflows the width of \
                the console. Defaults to `fold`.
            invert(`bool): Reverse the color gradient. Defaults to False.
            length(`int`): The number of colors in the gradient. Defaults to `3`.
            console(`MaxConsole`): The rich console to print \
                gradient text to. Defaults to MaxConsole().
            title(`str|Text'): The optional title of the Gradient. Defaults to 'Gradient'
            style(`StyleType`) The style of the gradient text. Defaults to None.
            bold(`bool`): Whether to bold the gradient text. Defaults to False.
            underline(`bool`): Whether to underline the gradient text. Defaults to False.
            italic(`bool`): Whether to italicize the gradient text. Defaults to False.
            rainbow(`bool`): Whether to print the gradient text in rainbow colors across \
                the spectrum. Defaults to False.
            string_end(`str`): The string to end the gradient text with. Defaults to \
                `\n`.
            verbose(`bool`): Whether to print verbose output. Defaults to False.
        """
        if isinstance(text, Text):
            text = str(text)
        super().__init__(text=text, justify=justify, overflow=overflow)
        self.console = console
        self.text = strip_control_codes(text)
        self.start_color = start
        self.end_color = end
        self.invert = bool(invert)
        self.length = length
        self.justify = justify
        self.indexes = []
        self.colors = []
        self.end = string_end
        self.title = title
        self.style = style
        self.bold = bold
        self.underline = underline
        self.italic = italic
        self.rainbow = rainbow
        self.verbose = verbose
        if self.style is not None:
            style = self.style.split(" ")

            if "bold" in style:
                self.bold = True
            if "underline" in style:
                self.underline = True
            if "italic" in style:
                self.italic = True

        if self.start_color in NamedColor.colors:
            self.start_color = NamedColor.colors.index(self.start_color)
        elif self.start_color in NamedColor.hex_colors:
            self.start_color = NamedColor.hex_colors.index(self.start_color)
        elif isinstance(self.start_color, NamedColor):
            self.start_color = NamedColor(self.start_color).as_index()
        elif isinstance(self.start_color, int):
            if self.start_color not in list(range(0, 9)):
                raise ValueError(
                    f"Invalid start index: {self.start_color}. Must be between 0 and 9."
                )
        elif self.start_color is None:
            pass
        else:
            raise TypeError(f"Invalid start type: {type(self.start_color)}")

        if not rainbow:
            if self.end_color in NamedColor.colors:
                self.end_color = NamedColor.colors.index(self.end_color)
            elif self.end_color in NamedColor.hex_colors:
                self.end_color = NamedColor.hex_colors.index(self.end_color)
            elif isinstance(self.end_color, NamedColor):
                self.end_color = NamedColor(self.end_color).as_index()
            elif isinstance(self.end_color, int):
                if self.end_color not in list(range(0, 9)):
                    raise ValueError(
                        f"Invalid end index: {self.end_color}. Must be between 0 and 9."
                    )
            elif self.end_color is None:
                pass
            else:
                raise TypeError(f"Invalid end type: {type(self.end_color)}")
        else:
            if self.start_color is None:
                self.start_color = 0
            if not invert:
                self.end_color = self.start_color - 1
                if self.end_color < 0:
                    self.end_color += 10
            else:
                self.end_color = self.start_color + 1
                if self.end_color > 9:
                    self.end_color -= 10

        if self.start_color is None and self.end_color is None:
            self.generate_start_end()
        elif self.start_color is None and self.end_color:
            self.generate_start()
        elif self.start_color and self.end_color is None:
            self.generate_end()
        else:
            self.generate_index()

        for index in self.indexes:
            self.colors.append(NamedColor.colors[index])

    def generate_start_end(self):
        """Generate the start and end when only `length` is provided."""
        self.start_color = randint(0, 9)
        self.indexes = []
        for index in range(self.length):
            if not self.invert:
                next_index = self.start_color + index
            else:
                next_index = self.start_color - index
            if next_index < 0:
                next_index += 10
            if next_index > 9:
                next_index -= 10
            self.indexes.append(next_index)
        self.end_color = self.indexes[-1]

    def generate_start(self):
        """Generate the start when only `end` is provided."""
        for index in range(self.length):
            if not self.invert:
                next_index = self.end_color - index
            else:
                next_index = self.end_color + index
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
                next_index = self.start_color + index
            else:
                next_index = self.start_color - index
            if next_index < 0:
                next_index += 10
            if next_index > 9:
                next_index -= 10
            self.indexes.append(next_index)
        self.end_color = self.indexes[-1]

    def generate_index(self):
        """Generate the index when both `start` and `end` are provided."""
        self.indexes = []
        if not self.invert:
            if self.start_color < self.end_color:
                self.length = (self.end_color + 1) - self.start_color
            else:
                self.length = (10 - self.start_color) + self.end_color + 1
        else:
            if self.start_color > self.end_color:
                self.length = (self.start_color + 1) - self.end_color
            else:
                self.length = (10 - self.end_color) + self.start_color + 1
        for index in range(self.length):
            if not self.invert:
                next_index = self.start_color + index
            else:
                next_index = self.start_color - index
            if next_index < 0:
                next_index += 10
            if next_index > 9:
                next_index -= 10
            self.indexes.append(next_index)
        assert next_index == self.end_color, f"{next_index} != {self.end_color}"

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

    def __len__(self) -> int:
        return len(self.text)

    def as_text(self) -> Text:
        """Return the gradient as a Text object."""
        size = len(self.text)
        number_of_gradients = int(self.length - 1)
        gradient_size = int(size // number_of_gradients)
        gradient_text = Text()

        for index in range(number_of_gradients):
            next_index = index + 1
            begin = index * gradient_size
            end = begin + gradient_size
            if index == number_of_gradients - 1:
                substring = Text(self.text[begin:])
            else:
                substring = Text(self.text[begin:end])

            if index < (self.length - 1):
                color1 = self.colors[index]
                r1, g1, b1 = tuple(NamedColor(color1).as_rgb())
                color2 = self.colors[next_index]
                r2, g2, b2 = tuple(NamedColor(color2).as_rgb())
                dr = r2 - r1
                dg = g2 - g1
                db = b2 - b1

            for x in range(len(substring)):
                blend = x / gradient_size
                color = f"#{int(r1 + dr * blend):02X}\
{int(g1 + dg * blend):02X}{int(b1 + db * blend):02X}"
                if self.bold:
                    bold = "bold "
                else:
                    bold = ""
                if self.underline:
                    underline = "underline "
                else:
                    underline = ""
                if self.italic:
                    italic = "italic "
                else:
                    italic = ""
                new_style = f"{bold}{underline}{italic} {color}"
                if "  " in new_style:
                    new_style = new_style.replace("  ", " ")
                mew_style = new_style.strip()
                substring.stylize(new_style, x, x + 1)

            if self.verbose:
                console.log(f"Gradient {index}:", substring)

            gradient_text = Text.assemble(
                gradient_text,
                substring,
                justify=self.justify,
                overflow=self.overflow,
                end=self.end_color,
            )
        return gradient_text

    def __rich__(self) -> RenderResult:
        """Rich representation of a gradient object."""
        return self.as_text()

    def __rich_console__(
        self, console: MaxConsole, options: ConsoleOptions
    ) -> RenderResult:
        """Rich representation of a gradient object."""
        return self.as_text()

    def __call__(self) -> Text:
        """Return the gradient as a Text object."""
        return self.as_text()

    def wrap(  # pylint: disable=arguments-renamed, arguments-differ
        self,
        width: int,
        justify: JustifyMethod = DEFAULT_JUSTIFY,
        overflow: OverflowMethod = DEFAULT_OVERFLOW,
        console: MaxConsole = MaxConsole(),
    ) -> Lines:
        """Wrap the gradient to a given width."""
        return self.as_text().wrap(
            console, width=width, justify=justify, overflow=overflow
        )


if __name__ == "__main__":
    console = MaxConsole()
    register_repr(Gradient)(normal_repr)
    register_repr(ColorIndex)(normal_repr)
    # console.clear()
    console.line(2)

    text1 = lorem.paragraphs(10)
    console.rule(title="Random Gradient", style="bold.white")
    gradient1 = Gradient(text1, title="Gradient <Random>")
    gradient1 = gradient1.wrap(125)
    console.print(gradient1, justify="center")
    console.line(2)

    text2 = lorem.paragraphs(10)
    console.rule(
        title="[bold white]Gradient <[/][bold.red]Red[/][bold.white] to \
[/][bold.blue]Light_Blue[/][bold.white]>[/]",
        style="bold.white",
    )
    gradient2 = Gradient(text2, justify="center", start="red", end="light_blue")
    console.print(gradient2, justify="left")
    console.line(2)

    title3 = "[underline bold.white]Inverted Italicized Bold Gradient <[/]"
    title3 = f"{title3}[bold.yellow]Yellow[/][bold.white] to[/]"
    title3 = f"{title3}[bold.blue]Blue[/][bold.white]>[/]"
    text3 = lorem.paragraphs(10)
    console.rule(
        title=title3,
        style="bold.white",
    )
    gradient3 = Gradient(
        text3,
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
    console.print(Gradient(text=text3, rainbow=True, bold=True), justify="right")
