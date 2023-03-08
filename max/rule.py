"""A gradient rule line for MaxConsole"""
# pylint: disable=unused-import
from random import randint
from typing import Optional

from rich.align import AlignMethod
from rich.cells import cell_len, set_cell_size
from rich.measure import Measurement
from rich.style import Style, StyleType
from rich.text import Text

from max.console import ConsoleOptions, MaxConsole, RenderResult
from max.gradient import Gradient


class GradientRule:  # pylint: disable=too-few-public-methods
    """A console renderable to draw a horizontal rule (line).

    Args:
        title (Optional[str|Text]): Text to render in the rule. Defaults to "".
        characters (Optional[str]): Character(s) used to draw the line. Defaults to "─".
        style (StyleType): Style of Rule. Defaults to "rule.line".
        end (str, optional): Character at end of Rule. defaults to "\\\\n"
        align (str, optional): How to align the title, one of "left", \
            "center", or "right". Defaults to "center".
    """

    def __init__(
        self,
        title: str | Text = "",
        *,
        title_style: str | Style | StyleType = "bold.white",
        style: Optional[str | Style | StyleType] = None,
        characters: str = "─",
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
        self.title_style = title_style
        self.style = style
        self.end = end
        self.align = align

    def __repr__(self) -> str:
        return f"MaxRule({self.title!r}, {self.characters!r})"

    def __rich_console__(
        self,
        console: MaxConsole,  # pylint: disable=redefined-outer-name
        options: ConsoleOptions,
    ) -> RenderResult:
        width = options.max_width

        characters = (
            "-"
            if (options.ascii_only and not self.characters.isascii())
            else self.characters
        )

        chars_len = cell_len(characters)
        if not self.title:
            yield self._gradient_rule_line(chars_len, width)
            return

        if isinstance(self.title, Text):
            title_text = self.title
        else:
            title_text = console.render_str(self.title, style=self.title_style)

        title_text.plain = title_text.plain.replace("\n", " ")
        title_text.expand_tabs()

        required_space = 4 if self.align == "center" else 2
        truncate_width = max(0, width - required_space)
        if not truncate_width:
            yield self._gradient_rule_line(chars_len, width)
            return

        rule_text = Text(end=self.end)
        if self.align == "center":
            title_text.truncate(truncate_width, overflow="ellipsis")
            side_width = (width - cell_len(title_text.plain)) // 2
            left = Text(characters * (side_width // chars_len + 1))
            left.truncate(side_width - 1)
            right_length = width - cell_len(left.plain) - cell_len(title_text.plain)
            right = Text(characters * (side_width // chars_len + 1))
            right.truncate(right_length)
            rule_text.append(left.plain + " ", self.style)
            rule_text.append(title_text)
            rule_text.append(" " + right.plain, self.style)

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
        rule_text = Gradient(rule_text)
        yield rule_text

    def _gradient_rule_line(self, chars_len: int, width: int) -> Text:
        rule_text = Text(self.characters * ((width // chars_len) + 1))
        rule_text.truncate(width)
        # rule_text.plain = set_cell_size(rule_text, width)
        gradient_rule_text = Gradient(rule_text)
        return gradient_rule_text

    def __rich_measure__(
        self,
        console: MaxConsole,  # pylint: disable=redefined-outer-name, unused-argument
        options: ConsoleOptions,  # pylint: disable=redefined-outer-name, unused-argument
    ) -> Measurement:
        return Measurement(1, 1)


if __name__ == "__main__":  # pragma: no cover
    import sys

    from max.console import MaxConsole  # pylint: disable=reimported

    try:
        TEXT = sys.argv[1]
    except IndexError:
        TEXT = "Hello, World"
    console = MaxConsole()
    console.print(GradientRule(title=TEXT))

    console = MaxConsole()
    console.print(GradientRule())
