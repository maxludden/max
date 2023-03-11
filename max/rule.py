"""A gradient rule line for MaxConsole"""
# pylint: disable=unused-import
# pylint: disable=unused-argument
import re
from random import randint
from typing import Optional

from rich import inspect
from rich.align import AlignMethod
from rich.cells import cell_len, set_cell_size
from rich.measure import Measurement
from rich.style import Style, StyleType
from rich.text import Text

from max.console import BaseMaxConsole as MaxConsole
from max.console import ConsoleOptions, RenderResult
from max.gradient import Gradient
from max.named_color import NamedColor


class GradientRule:  # pylint: disable=too-few-public-methods
    """A console renderable to draw a horizontal rule (line).
    Args:
        title (Optional[str, Text]): Text to render in the rule. Defaults to "".
        characters (str, optional): Character(s) used to draw the line. Defaults to "─".
        style (Optional[StyleType]): Style of Rule. Defaults to "rule.line".
        end (str, optional): Character at end of Rule. defaults to "\\\\n"
        align (str, optional): How to align the title, one of "left", "center", \
or "right". Defaults to "center".
    """

    def __init__(
        self,
        title: Optional[str | Text] = "",
        *,
        characters: str = "─",
        style: Optional[str | Style] = "rule.line",
        end: str = "\n",
        align: AlignMethod = "center",
    ) -> None:
        if cell_len(characters) < 1:
            raise ValueError(
                "'characters' argument must have a cell width of at least 1"
            )
        if align not in ("left", "center", "right"):
            raise ValueError(
                f'invalid value for align, expected "left", "center", "right" (not {align!r})'
            )
        self.title = title
        self.characters = characters
        self.style = style
        self.end = end
        self.align = align

    def __repr__(self) -> str:
        return f"GradientRule({self.title!r}, {self.characters!r})"

    def __rich__(self) -> RenderResult:
        width = console.options.max_width

        characters = (
            "-"
            if (console.options.ascii_only and not self.characters.isascii())
            else self.characters
        )

        chars_len = cell_len(characters)
        if not self.title:
            return self._rule_line(chars_len, width)

        if isinstance(self.title, Text):
            title_text = self.title
        else:
            title_text = console.render_str(self.title, style=self.style)

        title_text.plain = title_text.plain.replace("\n", " ")
        title_text.expand_tabs()

        required_space = 4 if self.align == "center" else 2
        truncate_width = max(0, width - required_space)
        if not truncate_width:
            return self._rule_line(chars_len, width)

        rule_text = Text(end=self.end)
        if self.align == "center":
            title_text.truncate(truncate_width, overflow="ellipsis")
            side_width = (width - cell_len(title_text.plain)) // 2
            left = Text(characters * (side_width // chars_len + 1))
            left.truncate(side_width - 1)
            right_length = width - cell_len(left.plain) - cell_len(title_text.plain)
            right = Text(characters * (side_width // chars_len + 1))
            right.truncate(right_length)
            rule_text.append(left.plain + " ")
            rule_text.append(title_text)
            rule_text.append(" " + right.plain)
        elif self.align == "left":
            title_text.truncate(truncate_width, overflow="ellipsis")
            rule_text.append(title_text)
            rule_text.append(" ")
            rule_text.append(characters * (width - rule_text.cell_len), self.style)
        elif self.align == "right":
            title_text.truncate(truncate_width, overflow="ellipsis")
            rule_text.append(characters * (width - title_text.cell_len - 1), self.style)
            rule_text.append(" ")
            rule_text.append(title_text)

        rule_text.plain = set_cell_size(rule_text.plain, width)
        self._gradient_rule(rule_text)
        return Gradient(rule_text.plain)

    def _rule_line(self, chars_len: int, width: int) -> Text:
        rule_text = Text(self.characters * ((width // chars_len) + 1), self.style)
        rule_text.truncate(width)
        rule_text.plain = set_cell_size(rule_text.plain, width)
        return Gradient(rule_text.plain)

    def _gradient_rule(self, rule_text: Text):
        regex = re.compile(r"^(?P<left>─* )(?P<text>.*)(?P<right> ─*)$", re.I | re.M)
        matches = regex.match(rule_text.plain)
        groups = matches.groups()
        console.print(groups)


if __name__ == "__main__":  # pragma: no cover
    import sys

    from max.console import BaseMaxConsole as MaxConsole  # pylint: disable=reimported

    try:
        TEXT = sys.argv[1]
    except IndexError:
        TEXT = "Hello, World"
    console = MaxConsole()
    rule1 = GradientRule(title=TEXT, style="bold red")
    console.print(rule1)

    console = MaxConsole()
    console.print(GradientRule())
