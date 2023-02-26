"""Description: A class to represent a named color."""
import sys
import re
from functools import lru_cache
from pathlib import Path
from time import sleep
from typing import Any, Tuple

from cheap_repr import normal_repr, register_repr
from console import MaxConsole
from rich import inspect
from rich.box import ROUNDED
from rich.columns import Columns
from rich.console import NewLine
from rich.prompt import Confirm
from rich.table import Table
from rich.text import Text
# from snoop import snoop


class ColorParsingError(ValueError):
    """Raised when a color cannot be parsed."""


class InvalidHexColor(ValueError):
    """Raised when a hex color is not valid."""


class InvalidRGBColor(ValueError):
    """Raised when an RGB color is not valid."""


CWD = Path.cwd()
LOG = CWD / "logs" / "log.log"
VERBOSE = CWD / "logs" / "verbose.log"
HEX_RE_STR = r"^\#([0-9a-fA-F]{6})$|^ ([0-9a-fA-F]{6})$"
HEX_PATTERN = re.compile(HEX_RE_STR, re.MULTILINE)

console = MaxConsole()


def colorful_class(on_white: bool = False) -> Text:
    """Print the word "NamedColor" in a rainbow of colors.

    Args:
        on_white (`optional[bool]`): Whether to print the text \
            on a white background. Defaults to False.

    Returns:
        `Text`: The formatted string.
    """
    if on_white:
        background = " on #ffffff"
    else:
        background = ""
    colored_n = f"[bold #ff00ff{background}]N[/]"
    colored_a = f"[bold #af00ff{background}]a[/]"
    colored_m = f"[bold #5f00ff{background}]m[/]"
    colored_e = f"[bold #0000ff{background}]e[/]"
    colored_d = f"[bold #0088ff{background}]d[/]"
    colored_c = f"[bold #00ffff{background}]C[/]"
    colored_o1 = f"[bold #00ff00{background}]o[/]"
    colored_l = f"[bold #ffff00{background}]l[/]"
    colored_o2 = f"[bold #ff8800{background}]o[/]"
    colored_r = f"[bold #ff0000{background}]r[/]"
    named_color = Text.assemble(
        colored_n,
        colored_a,
        colored_m,
        colored_e,
        colored_d,
        colored_c,
        colored_o1,
        colored_l,
        colored_o2,
        colored_r,
    )
    return named_color


def format_rgb(rgb: Tuple[int, int, int]) -> Text:
    """Return a formatted colorized string to represent the tuple."""
    r_value, g_value, b_value = rgb
    left_par = Text.from_markup("[#ffffff]([/]")
    r_string = Text.from_markup(f"[#000000 on #ff0000]{r_value:>3},[/]")
    g_string = Text.from_markup(f"[#000000 on #00ff00]{g_value:>3},[/]")
    b_string = Text.from_markup(f"[#ffffff on #0000ff]{b_value:>3}[/]")
    right_par = Text.from_markup("[#ffffff])[/]")
    return Text.assemble(
        left_par, r_string, g_string, b_string, right_par, justify="center"
    )


# ============================================================================ #
# NamedColor Class Definition
# ============================================================================ #


# lru_cache(maxsize=10)


class NamedColor:
    """Ten colors that span the spectrum to create gradients from."""

    _value: str
    _original: Any
    indexes: Tuple[int, ...] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    colors: Tuple[str, ...] = (
        "magenta",
        "light_purple",
        "purple",
        "blue",
        "light_blue",
        "cyan",
        "green",
        "yellow",
        "orange",
        "red",
    )
    hex_colors: Tuple[str, ...] = (
        "#ff00ff",
        "#af00ff",
        "#5f00ff",
        "#0000ff",
        "#0088ff",
        "#00ffff",
        "#00ff00",
        "#ffff00",
        "#ff8800",
        "#ff0000",
    )
    rgb_tuples: Tuple[Tuple[int, int, int], ...] = (
        (255, 0, 255),  # magenta
        (175, 0, 255),  # light_purple
        (95, 0, 255),  # purple
        (0, 0, 255),  # blue
        (0, 136, 255),  # light_blue
        (0, 255, 255),  # cyan
        (0, 255, 0),  # green
        (255, 255, 0),  # yellow
        (255, 136, 0),  # orange
        (255, 0, 0),  # red
    )

    # @snoop(watch_explode=("self", "color_input"))
    def __init__(self, color_input: Any, verbose: bool=False) -> None:
        # Parse NamedColor from inputs
        if isinstance(color_input, str):
            if color_input in self.colors:
                self.value = color_input
                self._original = color_input
                if verbose:
                    console.log("New color type: [#00ffff]str[/]-[bold #a500ff]color[/]")
                    console.log(f"New color: {color_input}")

            # HEX Colors
            elif HEX_PATTERN.match(color_input):
                try:
                    index = self.hex_colors.index(color_input)
                    self.value = self.colors[index]
                    self._original = color_input
                    if verbose:
                        console.log("New color type: [#00ffff]str[/]\
                            -[bold #a500ff]hex[/]")
                        console.log(f"New color: {color_input}")
                except InvalidHexColor as ihc:
                    raise InvalidHexColor("Unable to parse hex color", ihc) from ihc
        # RGB Tuple
        elif isinstance(color_input, tuple):
            try:
                index = self.rgb_tuples.index(color_input)
                self.value = self.colors[index]
                self._original = color_input
                if verbose:
                    console.log("New color type: [#00ffff]Tuple[/]\
                        -[bold #a500ff]RGB[/]")
                    console.log(f"New color: {color_input}")
            except InvalidRGBColor as irc:
                raise InvalidRGBColor("Unable to parse RGB color", irc) from irc

        # Index
        elif isinstance(color_input, int):
            if color_input in list(range(0, 10)):
                self.value = self.colors[color_input]
                self._original = color_input
                if verbose:
                    console.log("New color type: [#00ffff]Int[/]\
                        -[bold #a500ff]RGB[/]")
                    console.log(f"New color: {color_input}")
            else:
                raise ValueError(
                    f"Color Index must be between zero and nine. Input: {color_input}"
                )

        # NamedColor
        elif isinstance(color_input, NamedColor):
            self.value(color_input.value())
            self._original = color_input._original
            if verbose:
                console.log("New color type: [#0fffff]NamedColor[/]")
                console.log(f"New color type: {color_input}")
        else:
            raise ColorParsingError(
                "invalid_named_color", f"{color_input} is not a named color."
            )

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"<NamedColor: {self.value}>"

    def __rich_repr__(self) -> str:
        nc_color = colorful_class()
        return f"{nc_color}: [bold {self.as_hex()}]{str(self.value).capitalize()}[/]"

    @classmethod
    def get_all_colors(cls) -> set[dict[str, int | str | tuple]]:
        """Return a set of:
        - all colors('str')
        - their indexes(`int`)
        - hex values('str')
        - rgb values('tuple[int, int, int]')"""
        return list(zip((cls.colors, cls.indexes, cls.hex_colors, cls.rgb_tuples)))

    @property
    def value(self):
        """The `name` value of a color. Valid values are:
        - 'magenta',
        - 'light_purple',
        - 'purple,
        - 'blue',
        - 'light_blue',
        - 'cyan',
        - 'green',
        - 'yellow',
        - 'orange',
        - 'red'"""
        inspect(self)
        return self.value()

    @value.setter
    def value(self, value: Any) -> None:
        """The setter method for setting a NamedColor's value property."""
        if not value in self.colors:
            raise ColorParsingError(f"Invalid color value: {value}")
        self._value = value

    def named_color_table(self) -> Table:
        """Generate a table to display the named colors."""
        table = Table(
            f"{'Color':<12}",
            f"{'Index':^7}",
            f"{'Hex':^7}",
            f"{'RGB':^20}",
            title="All Colors",
            show_lines=True,
            header_style="reverse",
            expand=True,
            border_style="bold #ffffff",
        )
        for color in self.get_all_colors():
            name_value = color["color"]
            index_value = str(color["index"])
            hex_value = color["hex"]
            rgb_value = color["rgb"]

            if index_value in [1, 2, 3, 4, 9]:
                table.add_row(
                    (name_value, str(index_value), hex, str(rgb_value)),
                    style=f"bold #ffffff on {color[{hex_value}]}",
                )
            else:
                table.add_row(
                    color["color"],
                    str(color["index"]),
                    color["hex"],
                    str(color["rgb"]),
                    style=f"bold #000000 on {color['hex']}",
                )

    @lru_cache(maxsize=10)
    def as_index(self) -> int:
        """Retrieve the index of a color given its name."""
        match self.value:
            case "magenta":
                return 0
            case "light_purple":
                return 1
            case "purple":
                return 2
            case "blue":
                return 3
            case "light_blue":
                return 4
            case "cyan":
                return 5
            case "green":
                return 6
            case "yellow":
                return 7
            case "orange":
                return 8
            case "red":
                return 9
            case _:
                raise ValueError("Unable to convert NamedColor ({self}) to an integer")

    @lru_cache(maxsize=10)
    def as_hex(self) -> str:
        """Returns the Hex string of the NamedColor."""
        match self._value:
            case "magenta":
                return "#ff00ff"
            case "light_purple":
                return "#af00ff"
            case "purple":
                return "#5f00ff"
            case "blue":
                return "#0000ff"
            case "light_blue":
                return "#0088ff"
            case "cyan":
                return "#00ffff"
            case "green":
                return "#00ff00"
            case "yellow":
                return "#ffff00"
            case "orange":
                return "#ff8800"
            case "red":
                return "#ff0000"

    @lru_cache(maxsize=10)
    def as_rgb(self) -> Tuple[int, int, int]:
        """Returns the RGB Tuple of the Named Color."""
        match self._value:
            case "magenta":
                return (255, 0, 255)
            case "light_purple":
                return (175, 0, 255)
            case "purple":
                return (95, 0, 255)
            case "blue":
                return (0, 0, 255)
            case "light_blue":
                return (0, 136, 255)
            case "cyan":
                return (0, 255, 255)
            case "green":
                return (0, 255, 0)
            case "yellow":
                return (255, 255, 0)
            case "orange":
                return (255, 128, 0)
            case "red":
                return (255, 0, 0)

    def as_formatted_rgb(self) -> Text:
        """Return a formatted colorized string to represent the tuple."""
        r_value, g_value, b_value = tuple(self.as_rgb())
        left_par = Text.from_markup("[bold #ffffff]([/]")
        r_string = Text.from_markup(f"[bold #000000 on #ff0000]{r_value:>3},[/]")
        g_string = Text.from_markup(f"[bold #000000 on #00ff00]{g_value:>3},[/]")
        b_string = Text.from_markup(f"[bold #ffffff on #0000ff]{b_value:>3}[/]")
        end = Text.from_markup("[bold #ffffff])[/]")
        return Text.assemble(
            left_par, r_string, g_string, b_string, end, justify="center"
        )

    def __rich__(self):
        """Return whatever input was given to instantiate the\
            NamedColor object via rich's console protocol."""
        index = self.as_index()
        original_input = str(self._original)

        table = Table(
            title=f"{colorful_class()}[bold {self.as_hex()}]: {str(self._value).capitalize()}[/]",
            box=ROUNDED,
            expand=True,
            header_style=f"bold #ffffff on {self.as_hex()}",
            border_style=f"{self.as_hex()}",
            collapse_padding=True,
        )

        table.add_column(f"[{self.as_style()}]Original Color[/]", justify="center")
        table.add_column(f"[{self.as_style()}] Index[/]", justify="center")
        table.add_column(f"[{self.as_style()}]HEX[/]", justify="center")
        table.add_column(f"[{self.as_style()}]RGB[/]", justify="center")
        if index in [1, 2, 3, 4, 9]:
            table.add_row(
                f"[bold {self.as_hex()}]{str(original_input).capitalize()}[/]",
                f"[bold #ffffff]{index:^7}[/]",
                f"[bold #ffffff on {self.as_hex()}]{self.as_hex()}[/]",
                self.as_formatted_rgb(),
            )
        else:
            table.add_row(
                f"[bold {self.as_hex()}]{str(original_input).capitalize()}[/]",
                f"[bold #ffffff]{index:^7}[/]",
                f"[bold #000000 on {self.as_hex()}]{self.as_hex():^7}[/]",
                self.as_formatted_rgb(),
            )
        return table


    def as_style(self) -> str:
        """Returns the Style string of the NamedColor"""
        if self.as_index() in [1, 2, 3, 4, 9]:
            return f"bold #ffffff on {self.as_hex()}"
        elif self.as_index() in [0,5,6,7,8]:
            return f"bold #000000 on {self.as_hex()}"

    @classmethod
    def hex_to_rgb(cls, hex_value: str) -> Tuple:
        """
        Convert a hex color to rgb.
        Args:
            hex (str): The hex color.
        Returns:
            rgb (tuple): The rgb color.
        """
        if "#" in hex_value:
            stripped_hex = hex_value.replace("#", "")
        else:
            stripped_hex = hex_value
        rgb = []
        for i in (0, 2, 4):
            decimal = int(stripped_hex[i : i + 2], 16)
            rgb.append(decimal)
        return tuple(rgb)

    @classmethod
    def rgb_to_hex(cls, rgb: Tuple[int, int, int]) -> str:
        """Convert an rgb color to hex."""
        r_value, g_value, b_value = rgb

        return f"{r_value:X}{g_value:X}{b_value:X}"

    @staticmethod
    def colorful_class(on_white: bool = False) -> Text:
        """Print the word "NamedColor" in a rainbow of colors.

        Args:
            on_white (`optional[bool]`): Whether to print the text \
                on a white background. Defaults to False.

        Returns:
            `Text`: The formatted string.
        """
        if on_white:
            background = " on #ffffff"
        else:
            background = ""
        colored_n = f"[bold #ff00ff{background}]N[/]"
        colored_a = f"[bold #af00ff{background}]a[/]"
        colored_m = f"[bold #5f00ff{background}]m[/]"
        colored_e = f"[bold #0000ff{background}]e[/]"
        colored_d = f"[bold #0088ff{background}]d[/]"
        colored_c = f"[bold #00ffff{background}]C[/]"
        colored_o1 = f"[bold #00ff00{background}]o[/]"
        colored_l = f"[bold #ffff00{background}]l[/]"
        colored_o2 = f"[bold #ff8800{background}]o[/]"
        colored_r = f"[bold #ff0000{background}]r[/]"
        named_color = Text.assemble(
            colored_n,
            colored_a,
            colored_m,
            colored_e,
            colored_d,
            colored_c,
            colored_o1,
            colored_l,
            colored_o2,
            colored_r,
        )
        return named_color


register_repr(NamedColor)(normal_repr)


def print_color_tables(
    as_columns: bool = False, example_console: MaxConsole = console
) -> None:
    """A demo of the NamedColor class.

    Args:
        as_columns (bool, optional): Whether to print the colors as columns. Defaults to False.
        example_console (MaxConsole, optional): The console to print to. Defaults to console.
    """
    explanation = Text("NamedColor is a class that allows you to use named ")
    explanation_parts = [
        "colors in your code. The following colors are the NamedColors that ",
        "maxcolor makes gradients from. It also has a few extra methods to ",
        "help you work with the color.",
    ]
    for part in explanation_parts:
        explanation = Text.assemble(explanation, part)
    explanation = explanation.wrap(console=example_console, width=100, justify="left")
    console.clear()
    console.line(2)
    console.rule(title=f"{colorful_class(on_white=False)}", style="bold #ff00ff")
    console.line()
    console.print(
        explanation,
        justify="center",
    )
    console.print(NewLine(2))
    if as_columns:
        named_colors = [NamedColor(color, True) for color in NamedColor.colors]
        console.print(
            Columns(named_colors, equal=True, expand=True, column_first=True),
            justify="center",
        )
        console.print(NewLine(2))
    else:
        for color in NamedColor.colors:
            console.print(NamedColor(color), justify="center")
            console.print(NewLine(2))

if __name__ == "__main__":
    print_color_tables(as_columns=True)
    sleep(1)
    Confirm.ask(
        "Press [bold #00ff00]Enter[/] to exit...",
        console=console,
        show_choices=True,
        show_default=True,
        default=True,
    )
    sys.exit(0)
