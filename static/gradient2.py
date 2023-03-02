"""This module contains the gradient class to automate the creation of gradient colored text."""
# pylint: disable=W0611:unused-import
# pylint: disable=C0103:invalid-name
# pylint: disable=W0612:unused-variable
# pylint: disable=too-many-arguments
from os import environ
from random import randint
from typing import Optional, Tuple

from cheap_repr import ReprHelper, normal_repr, register_repr, try_register_repr
from lorem_text import lorem
from rich import inspect
from rich.console import JustifyMethod, RenderResult
from rich.control import strip_control_codes
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

    # @snoop
    def __init__(
        self,
        console: MaxConsole = MaxConsole(),  # pylint: disable=W0621:redefined-outer-name
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
            end_index = self._start_index + length
            self._end_index = self.fix_out_of_index(end_index)
        elif self.end is None:
            self._start_index = NamedColor(self.start).as_index()
            end_index = self._start_index + length
            self._end_index = self.fix_out_of_index(end_index)
        elif self.start is None:
            self._end_index = NamedColor(self.end).as_index()
            start_index = self._end_index + length
            self._start_index = self.fix_out_of_index(start_index)
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
        inspect(self)

        self.colors = []
        for index in self.indexes:
            self.colors.append(NamedColor(index))
        # inspect(self)

    @snoop(watch=["self.colors", "color_str"])
    def __str__(self) -> str:
        console.print(self.colors)
        color_str = ", ".join(f"{self.colors}")
        return f"Gradient<{color_str}>"

    def __repr__(self) -> str:
        return str(self)

    @debug()
    def __rich__(self) -> RenderResult:
        text = self.text
        size = len(text)
        gradient_size = size // self.length
        num = self.length - 1

        for index in range(1, num + 1):
            next_index = index + 1
            begin = index * gradient_size
            end = begin + gradient_size
            substring = text[begin:end]
            gradient_text = Text()

            if index < num - 1:
                r1, g1, b1 = tuple(NamedColor(self.colors[index]).as_rgb())
                # r1, g1, b1 = tuple(color1)
                r2, g2, b2 = tuple(NamedColor(self.colors[next_index]).as_rgb())
                # r2, g2, b2 = tuple(color2)

                dr = r2 - r1
                dg = g2 - g1
                db = b2 - b1

            for index in range(gradient_size):
                blend = index / gradient_size
                color = f"#{int(r1 + dr * blend):02X}\
                    {int(g1 + dg * blend):02X}\
                        {int(b1 + db * blend):02X}"  # type: ignore
                substring.stylize(color, index, index + 1)
                # log.success(f"color: {color} | index: {index} | substring: {substring}")

            gradient_text = Text.assemble(
                gradient_text, substring, justify=self.justify
            )
            return gradient_text

    @staticmethod
    def fix_out_of_index(index: int) -> int:
        """Fix out of index color indexes."""
        if index > 9:
            return index - 10
        if index < 0:
            return index + 10
        return index


register_repr(Gradient)(normal_repr)

if __name__ == "__main__":
    console = MaxConsole()
    register_repr(Gradient)(normal_repr)
    register_repr(ColorIndex)(normal_repr)
    console.clear()
    console.line(2)

    text1 = lorem.paragraph()
    console.log(f"Text: {text1}")
    gradient1 = Gradient(text1, title="Gradient <Random>")
    console.print(gradient1, justify="center")

    # text2 = lorem.paragraph()
    # gradient2 = Gradient(lorem.paragraph(), start="red", title="Gradient <Start: Red>")
    # console.print(gradient2, justify="center")

    # text3 = lorem.paragraph()
    # gradient3 = Gradient(
    #     lorem.paragraph(),
    #     end="green",
    #     invert=True,
    #     title="Gradient <End: Green, Inverted>",
    # )
    # console.print(gradient3, justify="center")
