# max/color_index.py
"""This module defines a the index from which to generate gradient text."""
import re
from itertools import cycle
from pathlib import Path
from random import choice, randint
from typing import Optional

from loguru import logger as log
from rich.console import NewLine
from rich.panel import Panel
from rich.text import Text

# from snoop import snoop

from max.console import MaxConsole
from max.progress import MaxProgress

console = MaxConsole()
progress = MaxProgress(console=console)


class InvalidHexColor(ValueError):
    """Raised when a hex color is invalid."""


class InvalidRGBColor(ValueError):
    """Raised when a RGB color is invalid."""

CWD = Path.cwd()
LOG = CWD / "logs" / "log.log"
VERBOSE = CWD / "logs" / "verbose.log"
HEX_RE_STR = r"^\#([0-9a-fA-F]{6})$|^ ([0-9a-fA-F]{6})$"
HEX_PATTERN = re.compile(HEX_RE_STR, re.MULTILINE)
TEST = False

log.remove()
log.configure(
    handlers=[
        dict(
            sink=lambda msg: console.log(
                msg,
                sep='|',
                style='logging.level.success'
                highlight=True
            )
            level="INFO"
        ),
        dict(
            sink=LOG,
            level="DEBUG"
        )
    ]
)




class ColorIndex:
    """
    A class to generate a list of indexes for a color wheel.

    Args:
        `start` (int, optional): The starting index. Defaults to None.
        `end` (int, optional): The ending index. Defaults to None.
        `invert` (bool, optional): If True, the indexes will be inverted. Defaults to False.
        `num_of_index` (int, optional): The number of indexes. Defaults to 3.
        `title` (str, optional): The title of the `ColorIndex` object. Defaults to "ColorIndex".
    """

    def __init__(
        self,
        start: Optional[int] = None,
        end: Optional[int] = None,
        invert: Optional[bool] = False,
        num_of_index: Optional[int] = 3,
        title: Optional[str] = "ColorIndex",
    ):
        self.start = start
        self.end = end
        self.invert = invert
        self.num_of_index = num_of_index
        self.title = title

        # Num of Index
        if not isinstance(self.num_of_index, int):
            raise TypeError(
                f"num_of_index must be an integer: {type(self.num_of_index)}"
            )
        if self.num_of_index not in list(range(2, 10)):
            raise ValueError(
                f"num_of_index must be between 2 and 9: {self.num_of_index}"
            )
        log.debug(f"Num of Index: {self.num_of_index}")

        # Start
        if self.start is None:
            self.start = randint(0, 9)
        if not isinstance(self.start, int):
            raise TypeError(f"Start must be an integer: {type(self.start)}")
        if self.start not in list(range(0, 10)):
            raise ValueError(f"Start must be between 0 and 9: {self.start}")
        log.debug(f"Start: {self.start}")

        if self.invert is None:
            self.invert = choice([True, False])
        if not isinstance(self.invert, bool):
            raise TypeError(f"invert must be a boolean: {type(self.invert)}")
        log.debug(f"Invert: {self.invert}")

        numbers = []
        for index in range(10):
            if not self.invert:
                num = self.start + index
                if num > 9:
                    num -= 10
            else:
                num = self.start - index
                if num < 0:
                    num += 10
            numbers.append(num)
        self.cycle = cycle(numbers)
        cycle_list = []
        for _ in range(10):
            cycle_list.append(next(self.cycle))
        log.debug(f"Cycle: {cycle_list}")

        # End
        if self.end is None:
            self.end = cycle_list[self.num_of_index]

        elif not isinstance(self.end, int):
            raise ValueError(f"end must be an integer: {self.end}")
        elif self.end not in list(range(0, 10)):
            raise ValueError(f"end must be between 0 and 9: {self.end}")
        log.debug(f"end: {self.end}")

        end_index = cycle_list.index(self.end)
        self.indexes = cycle_list[0 : end_index + 1]
        log.debug(f"Indexes: {self.indexes}")

    def colorful_class(self, on_white=False) -> Text:
        """Prints `ColorIndex' in a colorful way, manually.

        Args:
            `on_white` (bool, optional): If True, the background will be white. Defaults to False.
        """
        if on_white:
            background = " on #ffffff"
        else:
            background = ""
        colored_c = f"[bold #ff00ff{background}]C[/]"
        colored_o1 = f"[bold #af00ff{background}]o[/]"
        colored_l = f"[bold #5f00ff{background}]l[/]"
        colored_o2 = f"[bold #0000ff{background}]o[/]"
        colored_r = f"[bold #249df1{background}]r[/]"
        colored_i = f"[bold #00ffff{background}]I[/]"
        colored_n = f"[bold #00ff00{background}]n[/]"
        colored_d = f"[bold #ffff00{background}]d[/]"
        colored_e = f"[bold #ff8800{background}]e[/]"
        colored_x = f"[bold #ff0000{background}]x[/]"
        colored_index = f"{colored_c}{colored_o1}{colored_l}{colored_o2}{colored_r}\
            {colored_i}{colored_n}{colored_d}{colored_e}{colored_x}"
        return colored_index

    def __len__(self) -> int:
        return len(self.indexes)

    def __rich__(self) -> Panel:
        colors = [
            "#ff00ff",
            "#a900ff",
            "#5e00ff",
            "#1300ff",
            "#00aaff",
            "#00ffff",
            "#00ff00",
            "#ffff00",
            "#ffa900",
            "#ff0000",
        ]
        if self.title == "Color Index":
            title = self.colorful_class()
        else:
            title = self.title
        index_list = []
        for i in self.indexes:
            hex_colors = colors[i]
            index = f"[bold {hex_colors}]{i}[/]"
            index_list.append(index)
        indexes = "[bold #ffffff],[/] ".join(index_list)
        index_text = f"[bold #ffffff]< [/]{indexes} [bold #ffffff]>[/]"

        return Panel(index_text, title=title, border_style="bold #ffffff")

    @classmethod
    def demo(cls):
        """Prints a demo of `ColorIndex' to the console."""
        console = MaxConsole()
        console.clear()
        console.print(NewLine(2))
        color_index = ColorIndex().colorful_class()
        text_block1 = f"""[bold #ffffff]{color_index} is a mapping of colors from which to build a gradient to integers [/][bold italic #00ffff]0[/] - [/][bold italic #00ffff]9[/][bold #ffffff]. To create one, you can specify: \n\
    - A [italic]starting index[/italic]([/bold #ffffff][italic #5e00ff]start[/][bold #ffffff]) 
    - A [italic]finishing index[/italic]([/bold #ffffff][italic #5e00ff]end[/][bold #ffffff]) 
    - The [italic]direction[/italic]([/bold #ffffff][italic #5e00ff]invert[/][bold #ffffff]) the index flows 
    - The length of the index ([/bold #ffffff][italic #5e00ff]num_of_int[/][bold #ffffff]). 

However, you don't need all of these arguments to make a {color_index}. To generate a random {color_index}, no arguments are required.\n\n{color_index}[bold #ff00ff] 1[/][bold #ffffff] is an example of one such random {color_index}:\n"""

        console.print(text_block1, justify="center")

        color_index1 = ColorIndex(title=f"{color_index} [bold #ff00ff]1[/]")
        color_index = color_index1.colorful_class()
        console.print(color_index)
        console.print(color_index1, justify="center")
        console.print(NewLine(2))

        text_block2 = f"""{color_index} [bold #ff00ff]2[/bold #ff00ff][bold #ffffff] was created with a [italic]starting value[/italic] of [/bold #ffffff][bold italic #00ffff]0[/bold italic #00ffff][bold #ffffff], and a [italic]finishing value[/italic] of [/bold #ffffff][bold italic #00ffff]9[/bold italic #00ffff][bold #ffffff], which spans the entire range of possible indexes using {color_index}.\n[/bold #ffffff]"""
        console.print(text_block2, justify="center")
        color_index2 = ColorIndex(0, 9, title=f"{color_index} [bold #ff00ff]2[/]")
        console.print(color_index2, justify="center")
        console.print(NewLine(2))

        text_block3 = f"{color_index} [bold #ff00ff]3[/bold #ff00ff]\
[bold #ffffff] demonstrates both an [italic]inverted[/italic] gradient \
as well as how an index that goes outside of the integers [/bold #ffffff]\
[bold italic #00ffff]0[/] - [bold italic #00fffff]9[/][bold #fffff], will \
return from the opposite end of the spectrum.[/bold #fffff]\n"
        console.print(text_block3, justify="center")
        color_index3 = ColorIndex(2, 8, True, title=f"{color_index} [bold #ff00ff]3[/]")
        console.print(color_index3, justify="center")

        text_block4 = f"\n[bold #ffffff]There is one final argument that \
            has yet to be mentioned though it has been demonstrated extensively. \
            That is the [/][bold italic #5e00ff]title[/] [bold #ffffff] which \
            is the name of the {color_index} displayed in the repr and \
    rich dunder methods.[/]"

        console.print(text_block4, justify="center")


if __name__ == "__main__":
    ColorIndex.demo()
