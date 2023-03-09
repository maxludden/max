"""This module creates a sequence of increasing or decreasing integers \
    from which to generate a gradient."""
# pylint: disable=unused-import,redefined-outer-name,syntax-error
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
from max.log import debug, log
from max.named_color import NamedColor
from max.progress import MaxProgress

console = MaxConsole()
ASCENDING = cycle(list(range(10)))
DESCENDING = cycle(list(range(9, -1, -1)))


class ColorIndex(list):
    """A list of indexes from which to generate a gradient."""

    indexes: list = []
    _iter_index: int = 0

    def __init__(
        self,
        start: Optional[int] = None,
        end: Optional[int] = None,
        invert: Optional[bool] = False,
        length: Optional[int] = 3,
        title: Optional[str | Text] = "ColorIndex",
    ) -> None:
        """Generate a list of integers from which to construct a gradient.

		Args:
			start (Optional[int]): The integer from which to start the index.
			end (Optional[int]): The integer to end the index.
			invert (Optional[bool]): Whether to descend the index. Defaults to False.
			length (Optional[int]): The number of integers in the index. This value is \
only used when `start`, `end`, or both are not provided. Defaults to 3.
"""
        super().__init__([])
        self.start = start
        self.end = end
        self.invert = invert
        self.length = length
        self.title = title

        if self.start is None and self.end is None:
            self.generate_start_end()
        elif self.start is None and self.end:
            self.generate_start()
        elif self.start and self.end is None:
            self.generate_end()
        else:
            self.generate_index()

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
        """ "Generate the start when only `end` is provided."""
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
        if "ColorIndex" in self.title:
            self.title = self.colorful_class()
        else:
            self.title = self.title
        index_list = []
        for i in self.indexes:
            hex_color = colors[i]
            index = f"[bold {hex_color}]{i}[/]"
            index_list.append(index)
        indexes = "[bold #ffffff],[/] ".join(index_list)
        index_text = f"[bold #ffffff]< [/]{indexes} [bold #ffffff]>[/]"

        return Panel(index_text, title=self.title, border_style="bold #ffffff")

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
        color_index2 = ColorIndex(
            start=0, end=9, title=f"{color_index} [bold #ff00ff]2[/]"
        )
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
