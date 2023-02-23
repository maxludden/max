"""This module contains the gradient class to automate the creation of gradient colored text."""
# pylint: disable=W0611:unused-import
# pylint: disable=C0103:invalid-name
# pylint: disable=W0612:unused-variable
import re
from os import environ
from typing import Optional, Tuple

from lorem_text import lorem
from rich.console import Console, ConsoleOptions, JustifyMethod, RenderResult
from rich.control import _CONTROL_STRIP_TRANSLATE, strip_control_codes
from rich.segment import Segment
from rich.text import Text
from rich.repr import Result
from rich import inspect
from snoop import snoop
from cheap_repr import register_repr, normal_repr

from max.color_index import ColorIndex
from max.console import MaxConsole
from max.log import log
from max.named_color import ColorParsingError, NamedColor


class Gradient:
    """This class creates gradient text from a list of colors. Those colors are:
    - Red
    - Orange
    - Yellow
    - Green
    - Cyan
    - Light_blue
    - Blue
    - Purple
    - Light-purple
    - Magenta
    """

    start_index: int
    end_index: int
    indexes: ColorIndex
    colors: list[NamedColor]
    console: MaxConsole
    _start: Optional[NamedColor | str | int]
    _end: Optional[NamedColor | str | int]
    _invert: Optional[bool]
    _title: Optional[str]

    def __init__(
        self,
        text: Optional[str | Text] = None,
        start: Optional[NamedColor | str | int] = None,
        end: Optional[NamedColor | str | int] = None,
        justify: Optional[JustifyMethod] = None,
        invert: Optional[bool] = False,
        num_of_colors: Optional[int] = 2,
        _console: MaxConsole = MaxConsole(),
        title: Optional[str] = "Gradient",
    ) -> None:
        """Initialize the Gradient object.

        Args:
            text (Optional[str|Text], optional): The text to apply the \
                gradient to. Defaults to None ("")
            start (Optional[NamedColor|str|int], optional): The starting \
                color. Defaults to None.
            end (Optional[NamedColor|str|int], optional): The ending \
                color. Defaults to None.
            justify (Optional[JustifyMethod], optional): The justification \
                of the gradient text. Defaults to None.
            invert (Optional[bool], optional): If True, the colors will \
                be inverted. Defaults to False.
            num_of_colors (Optional[int], optional): The number of \
                colors in the gradientH. Defaults to 2.
            title (Optional[str], optional): The title of the `Gradient` \
                object. Defaults to "Gradient".
        """

        # initialize attributes
        self.justify = justify
        self._invert = invert
        self.num_of_colors = num_of_colors
        self.console = _console
        self._title = title
        self.start_index = 0
        self.start_end = 0
        self.indexes = []
        self.colors = []

        # Validate text
        assert isinstance(
            text, (str, Text)
        ), f"Text must be a string or a rich.text.Text object, not {type(text)}"
        sanitized_text = strip_control_codes(text)
        self._text = [sanitized_text]

        # Validate the input colors
        valid_start = self.validate_color(start)
        valid_end = self.validate_color(end)
        _start = self.parse_color(start) if valid_start else None
        _end = self.parse_color(end) if valid_end else None

        # Parse the colors and generate the indexes
        if _start is None and _end is None:
            self.indexes = ColorIndex(
                start=None,
                end=None,
                invert=self._invert,
                num_of_index=num_of_colors + 1,
                title=self._title
            )
        elif _end is None:
            self.indexes = ColorIndex(
                start=_start.as_index(),
                end=None,
                invert=self._invert,
                num_of_index=num_of_colors + 1,
                title=self._title
            )
        elif _start is None:
            self.indexes = ColorIndex(
                start=None,
                end=_end.as_index(),
                invert=self._invert,
                num_of_index=num_of_colors + 1,
                title=self._title
            )
        else:
            self.indexes = ColorIndex(
                start=_start.as_index(),
                end=_end.as_index(),
                invert=self._invert,
                num_of_index=num_of_colors + 1,
                title=self._title,
            )
        # log.success(f"Gradient indexes: {self.indexes}")

        for index in self.indexes:
            self.colors.append(NamedColor(index))
        # End of __init__

    def __repr__(self) -> str:
        return str(self.gradient_colors)

    def gradient_colors(self) -> Text:
        """Print out a colored Text object with the gradient colors."""
        ending = Text(">", style="bold.white")
        comma = Text(", ", style="bold.white")
        colors = Text("Gradient<", style="bold.white")
        length = len(self.colors)
        for repr_index, color in enumerate(self.colors):
            named_color = NamedColor(color).value()
            color_name = str(color).capitalize()
            color_style = f"bold.{color.value}"
            color_text = Text(color_name, style=color_style)
            colors = colors.assemble(colors, color_text)
            if repr_index < length - 1:
                colors = colors.assemble(colors, comma)
            else:
                colors = colors.assemble(colors, ending)
        return colors

    def plain_text(self) -> str:
        """Get the plain text of the gradient object."""
        return "".join(self._text)

    def validate_color(
        self, color: NamedColor | str | int, verbose: Optional[bool] = False
    ) -> NamedColor:
        """Parse an user entered color.
        
        Args:
            color (NamedColor|str|int): The color to parse.
            verbose (Optional[bool]): Whether to log the parsing \
                process to conosle. Defaults to False.
            
        Returns:
            NamedColor: The parsed color.
        """
        if isinstance(color, (str, int, NamedColor)):
            valid = True
        else:
            valid = False
        if verbose:
            if valid:
                self.console.log(
                    f"[bold underline #00ff00]Color {color} is \
                        valid:thumbs_up_light_skin_tone:[/]"
                )
            else:
                self.console.log(
                    f"[bold underline #ff0000]Color {color} is \
                        invalid:thumbs_down_light_skin_tone:[/]"
                )
        return valid

    @classmethod
    def parse_color(cls, color: NamedColor | str | int) -> NamedColor:
        """Parse an user entered color.

        Args:
            color (NamedColor|str|int): The color to parse.

        Returns:
            NamedColor: The parsed color.
        """
        try:
            return NamedColor(color)
        except ColorParsingError as cpe:
            raise ColorParsingError(
                f"Could not parse color {color}, error: {cpe}"
            ) from cpe

    # @snoop
    def __rich__(self) -> RenderResult:
        """Rich representation of the Gradient object."""

        console = MaxConsole()

        num_of_colors = len(self.colors)
        # console.log(f"Number of colors: {num_of_colors}")

        input_text = Text("".join(self._text))
        # console.log(f"Input Text: {input_text}")

        text_size = len(input_text)
        # console.log(f"Text Size: {text_size}")

        gradient_size = text_size // num_of_colors
        # console.log(f"Gradient Size: {gradient_size}\n\n")
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
    def split_text(text: str, num: int) -> list[Text]:
        """Split a text into equal parts.

        Args:
            text (str): The text to split.
            num (int): The number of parts to split the text into.

        Returns:
            list[str]: The split text.
        """
        text_size = len(text)
        gradient_size = text_size // num
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
        console = MaxConsole()
        text = Text(str(message))
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        dr = r2 - r1
        dg = g2 - g1
        db = b2 - b1
        size = len(text)
        for index in range(size):
            blend = index / size
            color = f"#{int(r1 + dr * blend):02X}"
            color = f"{color}{int(g1 + dg * blend):02X}"
            color = f"{color}{int(b1 + db * blend):02X}"
            text.stylize(color, index, index + 1)

        return text
register_repr(Gradient)(normal_repr)

if __name__ == "__main__":
    demo_console = MaxConsole(width=115)
    TEXT1 = lorem.paragraph()
    gradient1 = Gradient(TEXT1, "left")
    register_repr(Gradient)(normal_repr)
    demo_console.rule("Gradient1", style="bold.magenta")
    demo_console.print(gradient1, justify="center")
    demo_console.line(2)

    demo_console.rule("Gradient2", style="bold.magenta")
    TEXT2 = lorem.paragraph()
    demo_console.print(Gradient(TEXT2, "center"), justify="center")

    demo_console.rule("Gradient3", style="bold.magenta")
    demo_console.print(Gradient(TEXT2, "magenta", "red", "right"), justify="center")
