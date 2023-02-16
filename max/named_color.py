from pathlib import Path
from random import randint
from re import MULTILINE, compile
from sys import exit
from time import sleep
from typing import Any, Set, Tuple
from functools import lru_cache

from console import MaxConsole
from rich.box import ROUNDED
from rich.columns import Columns
from rich.console import Console, ConsoleOptions, NewLine
from rich.prompt import Confirm
from rich.table import Table
from rich.text import Text
from snoop import snoop, spy
from birdseye import eye
from cheap_repr import cheap_repr, register_repr


class ColorParsingError(ValueError):
    pass


class InvalidHexColor(ValueError):
    pass


class InvalidRGBColor(ValueError):
    pass


CWD = Path.cwd()
LOG = CWD / "logs" / "log.log"
VERBOSE = CWD / "logs" / "verbose.log"
HEX_RE_STR = r"^\#([0-9a-fA-F]{6})$|^ ([0-9a-fA-F]{6})$"
HEX_PATTERN = compile(HEX_RE_STR, MULTILINE)

console = MaxConsole()


def colorful_class(on_white: bool = False) -> Text:
    if on_white:
        background = " on #ffffff"
    else:
        background = ""
    N_ = f"[bold #ff00ff{background}]N[/]"
    A_ = f"[bold #af00ff{background}]a[/]"
    M_ = f"[bold #5f00ff{background}]m[/]"
    E_ = f"[bold #0000ff{background}]e[/]"
    D_ = f"[bold #249df1{background}]d[/]"
    C_ = f"[bold #00ffff{background}]C[/]"
    O1 = f"[bold #00ff00{background}]o[/]"
    L_ = f"[bold #ffff00{background}]l[/]"
    O2 = f"[bold #ff8800{background}]o[/]"
    R_ = f"[bold #ff0000{background}]r[/]"
    NAMEDCOLOR = f"{N_}{A_}{M_}{E_}{D_}{C_}{O1}{L_}{O2}{R_}"
    return NAMEDCOLOR


def format_rgb(rgb: Tuple[int, int, int]) -> Text:
    """Return a formatted colorized string to represent the tuple."""
    r, g, b = rgb
    left_par = Text.from_markup("[#ffffff]([/]")
    r_string = Text.from_markup(f"[#000000 on #ff0000]{r: >3},[/]")
    g_string = Text.from_markup(f"[#000000 on #00ff00]{g: >3},[/]")
    b_string = Text.from_markup(f"[#ffffff on #0000ff]{b: >3}[/]")
    right_par = Text.from_markup(f"[#ffffff])[/]")
    return Text.assemble(
        left_par, r_string, g_string, b_string, right_par, justify="center"
    )


# ============================================================================ #
# NamedColor Class Definition
# ============================================================================ #


lru_cache(maxsize=10)


class NamedColor:
    """Ten colors that span the spectrum to create gradients from."""

    value: str
    _original: Any

    indexes: Set[int] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    colors: Set[str] = (
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
    hex_colors: Set[str] = (
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
    rgb_tuples: Set[Tuple[int, int, int]] = (
        (255, 0, 255),  # magenta
        (175, 0, 255),  # light_purple
        (95, 0, 255),  # purple
        (0, 0, 255),  # blue
        (0, 136, 255),  # light_blue
        (0, 255, 255),  # cyan
        (0, 255, 0),  # green
        (255, 255, 0),  # yellow
        (255, 128, 0),  # orange
        (255, 0, 0),  # red
    )

    @spy
    @staticmethod
    def get_all_colors(self) -> set[dict[str, int | str | tuple]]:
        """Return a set of:
        - all colors('str')
        - their indexes(`int`)
        - hex values('str')
        - rgb values('tuple[int, int, int]')"""
        return list(zip((self.colors, self.indexes, self.hex_colors, self.rgb_tuples)))

    # all_colors = (
    #     {"color": "magenta", "index": 0, "hex": "#ff00ff", "rgb": (255, 0, 255)},
    #     {"color": "light_purple", "index": 1, "hex": "#af00ff", "rgb": (175, 0, 255)},
    #     {"color": "purple", "index": 2, "hex": "#5f00ff", "rgb": (5, 0, 255)},
    #     {"color": "blue", "index": 3, "hex": "#0000ff", "rgb": (0, 0, 255)},
    #     {"color": "light_blue", "index": 4, "hex": "#0088ff", "rgb": (0, 136, 255)},
    #     {"color": "cyan", "index": 5, "hex": "#00ffff", "rgb": (0, 255, 255)},
    #     {"color": "green", "index": 6, "hex": "#00ff00", "rgb": (0, 255, 0)},
    #     {"color": "yellow", "index": 7, "hex": "#ffff00", "rgb": (255, 255, 0)},
    #     {"color": "orange", "index": 8, "hex": "#ff8800", "rgb": (255, 128, 0)},
    #     {"color": "red", "index": 9, "hex": "#ff0000", "rgb": (255, 0, 0)},
    # )

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
            name = color["color"]
            index = str(color["index"])
            hex = color["hex"]
            rgb = color["rgb"]

            if index in [1, 2, 3, 4, 9]:
                table.add_row(
                    (name, str(index), hex, str(rgb)),
                    style=f"bold #ffffff on {color['hex']}",
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
    def __int__(self) -> int:
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
                raise ValueError(
                    "Unable to convert NamedColor ({self}) to an integer")

    def as_index(self) -> int:
        """Returns the index of the NamedColor"""
        return int(self)

    @lru_cache(maxsize=10)
    def as_hex(self) -> str:
        """Returns the Hex string of the NamedColor."""
        match self.value:
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
        match self.value:
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
        r, g, b = self.as_rgb()
        left_par = Text.from_markup("[#ffffff]([/]")
        r_string = Text.from_markup(f"[#000000 on #ff0000]{r: >3},[/]")
        g_string = Text.from_markup(f"[#000000 on #00ff00]{g: >3},[/]")
        b_string = Text.from_markup(f"[#ffffff on #0000ff]{b: >3}[/]")
        right_par = Text.from_markup(f"[#ffffff])[/]")
        return Text.assemble(
            left_par, r_string, g_string, b_string, right_par, justify="center"
        )

    def __init__(self, value: Any) -> None:
        # String of color in `.colors`
        if isinstance(value, str):
            if value in self.colors:
                self.value = value
                self._original = value

            # HEX Colors
            elif HEX_PATTERN.match(value):
                try:
                    index = self.hex_colors.index(value)
                    self.value = self.colors[index]
                    self._original = value
                except InvalidHexColor as ihc:
                    raise InvalidHexColor("Unable to parse hex color", ihc)
        # RGB Tuple
        elif isinstance(value, tuple):
            try:
                index = self.rgb_tuples.index(value)
                self.value = self.colors[index]
                self._original = value
            except InvalidRGBColor as irc:
                raise InvalidRGBColor("Unable to parse RGB color", irc)

        # Index
        elif isinstance(value, int):
            if value in list(range(0, 10)):
                self.value = self.colors[value]
                self._original = value
            else:
                raise ValueError(
                    f"Color Index must be between zero and nine. Input: {value}"
                )

        # NamedColor
        elif isinstance(value, NamedColor):
            self.value = value.value
            self._original = value._original
        else:
            raise ColorParsingError(
                "invalid_named_color", f"{value} is not a named color."
            )

    def __rich__(self):
        index = int(self)
        original_input = str(self._original)

        table = Table(
            title=f"{colorful_class()}[bold {self.as_hex()}]: {str(self.value).capitalize()}[/]",
            box=ROUNDED,
            expand=True,
            header_style=f"bold #ffffff on {self.as_hex()}",
            border_style=f"{self.as_hex()}",
            collapse_padding=True,
        )

        table.add_column(
            f"[{self.as_Style()}]Original Color[/]", justify="center")
        table.add_column("Index", justify="center")
        table.add_column("HEX", justify="center")
        table.add_column("RGB", justify="center")
        table.add_row(
            f"[bold {self.as_hex()}]{str(original_input).capitalize()}[/]",
            f"[bold #ffffff]{index}[/]",
            f"[bold #ffffff on {self.as_hex()}]{self.as_hex()}[/]",
            self.as_formatted_rgb(),
        ),
        return table

    def __repr__(self) -> str:
        return f"<NamedColor: {self.value}>"

    def __rich_repr__(self) -> str:
        nc_color = colorful_class()
        return f"{nc_color}: [bold {self.as_hex()}]{str(self.value).capitalize()}[/]"

    def __str__(self) -> str:
        return self.value

    def as_index(self) -> int:
        """Returns the index of the NamedColor"""
        return int(self)

    def as_hex(self) -> str:
        """Returns the hex value of the NamedColor"""
        return self.hex_colors[int(self)]

    def as_rgb(self) -> Tuple[int, int, int]:
        """Returns the RGB tuple of the NamedColor"""
        return self.rgb_tuples[int(self)]

    def as_formatted_rgb(self) -> Text:
        """Return a formatted colorized string to represent the tuple."""
        r, g, b = self.as_rgb()
        left_par = Text.from_markup("[#ffffff]([/]")
        r_string = Text.from_markup(f"[#000000 on #ff0000]{r: >3},[/]")
        g_string = Text.from_markup(f"[#000000 on #00ff00]{g: >3},[/]")
        b_string = Text.from_markup(f"[#ffffff on #0000ff]{b: >3}[/]")
        right_par = Text.from_markup(f"[#ffffff])[/]")
        return Text.assemble(
            left_par, r_string, g_string, b_string, right_par, justify="center"
        )

    def as_Style(self) -> str:
        """Returns the Style string of the NamedColor"""
        if self.as_index() in [1, 2, 3, 4, 9]:
            return f"bold #ffffff on {self.as_hex()}"
        else:
            return f"bold #ffffff on {self.as_hex()}"

    def hex_to_rgb(hex: str) -> Tuple:
        """
        Convert a hex color to rgb.
        Args:
            hex (str): The hex color.
        Returns:
            rgb (tuple): The rgb color.
        """
        if "#" in hex:
            stripped_hex = hex.replace("#", "")
        else:
            stripped_hex = hex

        if HEX_PATTERN.match(stripped_hex):
            rgb = []
            for i in (0, 2, 4):
                decimal = int(hex[i: i + 2], 16)
                rgb.append(decimal)
            return tuple(rgb)
        else:
            raise InvalidHexColor(f"Invalid hex color: {hex}")

    def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
        """Convert an rgb color to hex."""
        r, g, b = rgb

        return f"{r:X}{g:X}{b:X}"

    @classmethod
    def color_name(cls) -> Text:
        """Returns the classes name with each color progressing the named colors."""
        range = []
        start = randint(0, 9)
        for i in range(10):
            index = (start + i) % 10
            range.append(cls.colors[index])
        repeat = len(range)
        for x in range(repeat):
            range.append(range[x])


def print_color_tables(
    as_columns: bool = False, console: Console = MaxConsole()
) -> None:
    """A demo of the NamedColor class."""
    explanation = Text(
        "NamedColor is a class that allows you to use named colors in your code. The following colors are the NamedColors that maxcolor makes gradients from. It also has a few extra methods to help you work with the color."
    )
    explanation = explanation.wrap(console=console, width=60, justify="left")
    console = MaxConsole()
    console.clear()
    console.print(NewLine(2))
    console.rule(title=colorful_class(on_white=False), style="bold #ff00ff")
    console.print(NewLine(2))
    console.print(
        explanation,
        justify="center",
    )
    console.print(NewLine(2))
    if as_columns:
        named_colors = [NamedColor(color) for color in NamedColor.colors]
        console.print(
            Columns(named_colors, equal=True, expand=True, column_first=True),
            justify="center",
        )
        console.print(NewLine(2))
    else:
        for color in NamedColor.colors:
            console.print(NamedColor(color), justify="center")
            console.print(NewLine(2))


@register_repr(NamedColor)
def repr_my_class(x, helper):
    return helper.repr_iterable(x.items, "NamedColor([", "])")


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
    exit(0)
