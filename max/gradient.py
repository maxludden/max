"""This module contains the gradient class to automate the creation of gradient colored text."""
# pylint: disable=W0611:unused-import
# pylint: disable=C0103:invalid-name
# pylint: disable=W0612:unused-variable
# pylint: disable=too-many-arguments
import re
from dataclasses import dataclass
from os import environ
from typing import Optional, Tuple
from random import randint

from cheap_repr import normal_repr, register_repr
from lorem_text import lorem
from rich.console import JustifyMethod, RenderResult
from rich.control import strip_control_codes
from rich.text import Text
from snoop import snoop

from max.color_index import ColorIndex
from max.console import MaxConsole, Console
from max.log import debug, log
from max.named_color import (
    ColorParsingError,
    InvalidHexColor,
    InvalidRGBColor,
    NamedColor,
)


@dataclass
class Gradient:
    """Print gradient text to the console using `rich` library."""
    console = MaxConsole()
    text: str
    start: NamedColor
    end: NamedColor
    invert: bool = False
    length: int = 3
    title: Optional[str | Text]
    justify: JustifyMethod = "center"
    _start_index: int
    _end_index: int
    indexes = ColorIndex
    colors = list[NamedColor]

    def __init__(
        self,
        console: Console = MaxConsole(),
        text: str = "",
        start: Optional[NamedColor | str | int] = None,
        end: Optional[NamedColor | str | int] = None,
        invert: bool = False,
        length: int = 3,
        justify: JustifyMethod = "center",
        title: str = "Gradient",
    ) -> None:
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
        self.console = console
        self.text = strip_control_codes(text)
        self.start = start
        self.end = end
        self.invert = invert
        self.length = length
        self.justify = justify
        self.title = title

        if self.invert:
            length = length * -1

        if self.start is None and self.end is None:
            self._start_index = randint(0, 9)
            self._end_index = self._start_index + length
        elif self.end is None:
            self._start_index = NamedColor(self.start).as_index()
            self._end_index = self._start_index + length
        elif self.start is None:
            self._end_index = NamedColor(self.end).as_index()
            self._start_index = self._end_index - length
        else:
            self._start_index = NamedColor(self.start).as_index()
            self._end_index = NamedColor(self.end).as_index()

        self.indexes = tuple(
            ColorIndex(
                start=self._start_index,
                end=self._end_index,
                invert=self.invert,
                num_of_index=self.length,
                title=self.title,
            )
        )
        for index in self.indexes:
            self.colors.append(NamedColor(index))

    def __str__(self) -> str:
        color_angular = f"<{', '.join(self.colors)}>"
        return f"Gradient{color_angular}"

    def __repr__(self) -> str:
        return str(self)

    def __rich__(self) -> RenderResult:
        text = self.text
        size = len(text)
        gradient_size = size // self.length
        num = self.length - 1

        for index in range(num):
            next_index = index + 1
            begin = index * gradient_size
            end = begin + gradient_size
            _substring = text[begin:end]

            if index < num - 1:
                r1, g1, b1 = self.colors[index].as_rgb()
                r2, g2, b2 = self.colors[next_index].as_rgb()

                dr = r2 - r1
                dg = g2 - g1
                db = b2 - b1

            for index in range(gradient_size):
                blend = index / gradient_size
                color = f"#{int(r1 + dr * blend):02X}\
                    {int(g1 + dg * blend):02X}\
                        {int(b1 + db * blend):02X}"  # type: ignore
                _substring.stylize(color, index, index + 1)

            text = Text.assemble(text, _substring, justify="left")

if __name__ == "__main__":
    demo_console = MaxConsole()
    demo_console.print(
        Gradient(
            lorem.paragraph(),
        )
    )
