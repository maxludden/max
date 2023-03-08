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

    def __init__(
        self,
        start: Optional[int] = None,
        end: Optional[int] = None,
        invert: Optional[bool] = False,
        length: Optional[int] = 3,
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

        if self.start is None and self.end is None:
            self.start = randint(0, 9)
            self.indexes = [self.start]
            for index in range(self.length):
                if not self.invert:
                    next_index = start + index
                else:
                    next_index = start - index
                if index < 0:
                    next_index += 10
                if index > 9:
                    next_index -= 10
                self.indexes.append(next_index)
        elif self.start is None and self.end:
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
        elif self.start and self.end is None:
            for index in range(self.length):
                if not self.invert:
                    next_index = start + index
                else:
                    next_index = start - index
                if index < 0:
                    next_index += 10
                if index > 9:
                    next_index -= 10
                self.indexes.append(next_index)
        else self.start and self.end:
            self.length = 0
            self.