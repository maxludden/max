"""This module contains the gradient class to automate the creation of gradient colored text."""
# pylint: disable=W0611:unused-import
# pylint: disable=C0103:invalid-name
# pylint: disable=W0612:unused-variable
# pylint: disable=R0913:too-many-arguments
import re
from os import environ
from random import randint
from typing import Optional, Tuple

from cheap_repr import normal_repr, register_repr
from lorem_text import lorem
from rich.console import JustifyMethod, RenderResult
from rich.control import strip_control_codes
from rich.table import Table
from rich.text import Text
from snoop import snoop

from max.color_index import ColorIndex
from max.console import MaxConsole
from max.log import debug, log
from max.named_color import (
    ColorParsingError,
    InvalidHexColor,
    InvalidRGBColor,
    NamedColor,
)


class Gradient:
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

    # @snoop
    def __init__(
        self,
        text: Optional[str | Text] = None,
        start: Optional[NamedColor | str | int] = None,
        end: Optional[NamedColor | str | int] = None,
        justify: Optional[JustifyMethod] = None,
        invert: Optional[bool] = False,
        length: Optional[int] = 3,
        console: MaxConsole = MaxConsole(),  # pylint: disable=W0621:redefined-outer-name
        title: Optional[str] = "Gradient",
        verbose: Optional[bool] = False,
    ) -> None:
        """Print gradient colored text to the console.
        Args:
            text(`text): The text to print. Defaults to empty string.
            start(`NamedColor | str | int`): The color to start the gradient.
            end(`NamedColor|str|int`): The color to end the gradient.
            justify(`JustifyMethod`): How to align the gradient text locally. Defaults \
                to `left`.
            invert(`bool): Reverse the color gradient. Defaults to False.
            length(`int`): The number of colors in the gradient. Defaults to `3`.
            console(`MaxConsole`): The rich console to print \
                gradient text to. Defaults to MaxConsole().
            title(`str|Text'): The optional title of the Gradient. Defaults to 'Gradient'
        """
        self.console = console
        self.text = strip_control_codes(text)
        self.start = NamedColor(start)
        self.end = NamedColor(end)
        self.invert = invert
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
                console.log(
                    f"None-none: random start_index: {self.start.as_index()}\
 random end_index: {self.end.as_index()}"
                )

        elif self.end is None and self.start:
            if self.invert:
                end_index = self.start.as_index() + int(self.length)
            else:
                end_index = self.start.as_index() - int(self.length)
            self.end = NamedColor(end_index)
            if verbose:
                console.log(
                    f"start-none: random start_index: {self.start.as_index()}\
 random end_index: {self.end.as_index()}"
                )

        elif self.start is None and self.end:
            if self.invert:
                start_index = self.end.as_index() - int(self.length)
            else:
                start_index = self.end.as_index() + int(self.length)
            self.start = NamedColor(start_index)
            console.log(
                f"None-end: random start_index: {self.start.as_index()}\
 random end_index: {self.end.as_index}"
            )

        else:
            if verbose:
                self.console.log(f"\nstart: {self.start}\nend: {self.end}\n")
            if invert:
                if self.start.as_index() > self.end.as_index():
                    self.length = self.end.as_index() - self.start.as_index()
                else:
                    self.length = self.start.as_index() + (10 - self.end.as_index())
            else:
                if self.start.as_index() < self.end.as_index():
                    self.length = self.end.as_index() - self.end.as_index()
                else:
                    self.length = (10 - self.end.as_index()) + self.start.as_index()

        self.indexes = ColorIndex(
            start=self.start.as_index(),
            end=self.end.as_index(),
            invert=self.invert,
            num_of_index=self.length,
            title=self.title,
        )
        for index in self.indexes:
            self.colors.append(NamedColor(index))

    def __str__(self):
        return self.text

    def __repr__(self) -> str:
        return f"Gradient<{', '.join([str(color) for color in self.colors])}>"

    def __rich__(self) -> RenderResult:
        """Rich representation of the Gradient object."""
        num_of_colors = len(self.colors)
        input_text = Text("".join(self.text))
        text_size = len(input_text)
        gradient_size = text_size // num_of_colors
        gradient_text = Text()

        substrings = self.split_text(input_text, num_of_colors - 1)
        # console.log(f"Substrings: {substrings}")

        for x, substring in enumerate(substrings):
            if x < num_of_colors - 1:
                color1 = self.colors[x].as_rgb()
                color2 = self.colors[x + 1].as_rgb()
                substring = self.simple_gradient(substring, color1, color2)
            gradient_text = Text.assemble(
                gradient_text, substring, justify=self.justify
            )
        return gradient_text

    @staticmethod
    def simple_gradient(
        message: str, color1: Tuple[int, int, int], color2: Tuple[int, int, int]
    ) -> Text:
        """Blend text from one color to another. This function was found in rich-cli \
code and repurposed to make Gradient possible.

        Args:
            message (str): The text to apply the gradient to
            color1 (Tuple[int, int, int]): The first color of the gradient
            color2 (Tuple[int, int, int]): The second color of the gradient

        Returns:
            Text: The gradient text
        """
        text = Text(str(message))
        size = len(text)

        r1, g1, b1 = color1
        r2, g2, b2 = color2

        dr = r2 - r1
        dg = g2 - g1
        db = b2 - b1

        for index in range(size):
            blend = index / size
            color = f"#{int(r1 + dr * blend):02X}"
            color = f"{color}{int(g1 + dg * blend):02X}"
            color = f"{color}{int(b1 + db * blend):02X}"
            text.stylize(color, index, index + 1)

        return text

    @staticmethod
    def split_text(text: str, num: int) -> list[Text]:
        """Split a text into equal parts.

        Args:
            text (str): The text to split.
            num (int): The number of parts to split the text into.

        Returns:
            list[str]: The split text.
        """
        try:
            text_size = len(text)
            gradient_size = text_size // num
        except ZeroDivisionError as zde:
            num = 1
        substrings = []
        for index in range(num):
            begin = index * gradient_size
            end = begin + gradient_size
            if index == 0:
                substring = str(text[begin:end])
            else:
                substring = str(text[begin + 1 : end + 1])
            substring = Text(substring)
            substrings.append(substring)
        return substrings


if __name__ == "__main__":
    console = MaxConsole(width=125)
    register_repr(Gradient)(normal_repr)
    register_repr(ColorIndex)(normal_repr)
    console.clear()
    console.line(2)

    text1 = lorem.paragraph()
    console.rule(title="Random Gradient", style="bold.white")
    gradient1 = Gradient(text1, title="Gradient <Random>")
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
        title="[bold white]Inverted Gradient <[/][bold #ff0000]Red[/][bold white] to \
[/][bold #0000ff]Blue[/][bold white]>[/]",
        style="bold.white",
    )
    gradient3 = Gradient(text3, justify="center", start="red", end="blue", invert=True)
    console.print(gradient3, justify="center")
    console.line(2)
