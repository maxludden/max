"""This module creates a sequence of increasing or decreasing integers \
    from which to generate a gradient."""
# max/color_index.copy()
# pylint: disable=W0611:unused-import
from collections.abc import Sequence
from itertools import cycle
from os import environ
from pathlib import Path
from random import choice, randint
from typing import Optional

# from snoop import snoop
from cheap_repr import normal_repr, register_repr
from loguru import logger as log
from rich import inspect
from rich.panel import Panel
from rich.text import Text
from snoop import snoop

from max.console import MaxConsole
from max.log import debug
from max.named_color import NamedColor
from max.progress import MaxProgress

console = MaxConsole()
CWD = Path.cwd()
LOGS = CWD / "logs"
LOG = LOGS / "log.log"
FORMAT = environ.get("LOGURU_FORMAT")
RICH_SUCCESS_LOG_FORMAT = environ.get("RICH_SUCCESS_LOG_FORMAT")
RICH_ERROR_LOG_FORMAT = environ.get("RICH_ERROR_LOG_FORMAT")
ASCENDING = cycle(list(range(10)))
DESCENDING = cycle(list(range(9, -1, -1)))
TEST = True


class ColorIndex(Sequence):
    """
    A class to generate a list of indexes for a color wheel.

    Args:
        `start` (int, optional): The starting index. Defaults to None.
        `end` (int, optional): The ending index. Defaults to None.
        `invert` (bool, optional): If True, the indexes will be inverted. Defaults to False.
        `num_of_index` (int, optional): The number of indexes. Defaults to 3.
        `title` (str, optional): The title of the `ColorIndex` object. Defaults to "ColorIndex".
    """

    start: Optional[int]
    end: Optional[int]
    invert: Optional[bool]
    num_of_index: Optional[int]
    indexes: list[int]
    title: Optional[str]
    _iter_index: int

    # @snoop
    def __init__(
        self,
        start: Optional[int] = None,
        end: Optional[int] = None,
        invert: Optional[bool] = False,
        num_of_index: Optional[int] = 3,
        title: Optional[str] = "ColorIndex",
    ) -> None:
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
        if self.num_of_index < 2:
            self.num_of_index += 10
        if self.num_of_index > 10:
            self.num_of_index -= 10
        log.debug(f"Num of Index: {self.num_of_index}")

        # Start
        if self.start is None:
            self.start = randint(0, 9)
        if not isinstance(self.start, int):
            raise TypeError(f"Start must be an integer: {NamedColor(self.start)}")
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

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [self[i] for i in range(*index.indices(len(self)))]
        elif index < 0:
            index = len(self) + index
        if not 0 <= index < len(self):
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
        colored_index = Text.assemble(
            colored_c,
            colored_o1,
            colored_l,
            colored_o2,
            colored_r,
            colored_i,
            colored_n,
            colored_d,
            colored_e,
            colored_x,
        )
        return colored_index

    def __len__(self) -> int:
        return len(self.indexes)

    def __rich__(self) -> Panel:
        colors = [
            "#ff00ff",
            "#af00ff",
            "#6f00ff",
            "#0000ff",
            "#0088ff",
            "#00ffff",
            "#00ff00",
            "#ffff00",
            "#ff8800",
            "#ff0000",
        ]
        if self.title == "Color Index":
            title = self.colorful_class()
        else:
            title = self.title
        index_list = []
        for i in self.indexes:
            hex_color = colors[i]
            index = f"[bold {hex_color}]{i}[/]"
            index_list.append(index)
        indexes = "[bold #ffffff],[/] ".join(index_list)
        index_text = f"[bold #ffffff]< [/]{indexes} [bold #ffffff]>[/]"

        return Panel(index_text, title=title, border_style="bold #ffffff")

    @staticmethod
    def demo():
        """Generate a demonstration of the ColorIndex Class."""
        console.clear()
        console.line(2)
        color_index = ColorIndex().colorful_class()

        text_block1 = f"[bold #ffffff]{color_index} is a mapping of colors \
from which to build a gradient to \nintegers [/][bold italic #00ffff]0[/]\
[bold #ffffff] - [/][bold italic #00ffff]9[/][bold #ffffff]. To create one \
you can specify a [italic]starting index[/italic]([/bold #ffffff]\
[italic #af00ff]start[/][bold #ffffff]), a \n[italic]finishing index[/italic]\
([/bold #ffffff][italic #af00ff]end[/][bold #ffffff]), which [italic]\
direction[/italic] the index flows ([/bold #ffffff][italic #af00ff]\
invert[/][bold #ffffff]), or the \nlength of the index ([/bold #ffffff]\
[italic #af00ff]num_of_int[/][bold #ffffff]). However you don't need all \
of these arguments \nto make a {color_index}. To generate \
a random {color_index}, no arguments are required.[/bold #ffffff]\n\n\n{color_index}\
[bold #ff00ff] 1[/][bold #ffffff] is an example of one such random {color_index}:\n"
        console.print(text_block1, justify="center", width=115)

        color_index1 = ColorIndex(title=f"{color_index} [bold #ff00ff]1[/]")
        color_index = color_index1.colorful_class()
        # console.print(color_index)
        console.print(color_index1, justify="center", width=115)
        console.line(2)

        text_block2 = f"{color_index} [bold #ff00ff]2[/bold #ff00ff]\
[bold #ffffff] was created with a [italic]starting value[/italic] of [/bold #ffffff]\
[bold italic #00ffff]0[/bold italic #00ffff]\
[bold #ffffff], and a [italic]finishing value[/italic] of [/bold #ffffff]\
[bold italic #00ffff]9[/bold italic #00ffff]\
[bold #ffffff], which spans \nthe entire range of possible indexes \
using {color_index}.\n[/bold #ffffff]"
        console.print(text_block2, justify="center", width=115)
        color_index2 = ColorIndex(0, 9, title=f"{color_index} [bold #ff00ff]2[/]")
        console.print(color_index2, justify="center", width=115)
        console.line(2)

        text_block3 = f"{color_index} [bold #ff00ff]3[/bold #ff00ff]\
[bold #ffffff] demonstrates both an [italic]inverted[/italic] gradient \
as well as how an index that goes outside of \nthe integers [/bold #ffffff]\
[bold italic #00ffff]0[/] - [bold italic #00fffff]9[/][bold #fffff], will \
return from the opposite end of the spectrum.[/bold #fffff]\n"
        console.print(text_block3, justify="center", width=115)
        color_index3 = ColorIndex(2, 8, True, title=f"{color_index} [bold #ff00ff]3[/]")
        console.print(color_index3, justify="center", width=115)

        text_block4 = f"\n[bold #ffffff]There is one final argument that has yet to be mentioned \
though it has been demonstrated \nextensively. That is the [/][bold italic #af00ff]title[/]\
[bold #ffffff] which is the name of the {color_index} displayed in the repr \
and rich \ndunder methods.[/]\n\n\n"

        console.print(text_block4, justify="center", width=115)


register_repr(ColorIndex)(normal_repr)

if __name__ == "__main__":
    ColorIndex.demo()
