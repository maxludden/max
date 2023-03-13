"""A gradient rule line for MaxConsole"""

from random import randint
from typing import Optional

from rich.align import AlignMethod
from rich.cells import cell_len, set_cell_size
from rich.console import RenderResult, console
from rich.errors import MissingStyle
from rich.style import Style
from rich.text import Text

from max.console import MaxConsole
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
        thick (bool, optional): Draw a rule that is as think as possible. Defaults to False.
    """

    def __init__(
        self,
        title: Optional[str | Text] = "",
        gradient_title: bool = False,
        *,
        characters: str = "─",
        style: Optional[str | Style] = "bold.white",
        end: str = "\n",
        align: AlignMethod = "center",
        thick: bool = False,
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
        self.gradient_title = gradient_title
        self.characters = characters
        self.style = style
        self.end = end
        self.align = align
        self.thick = thick

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
            try:
                console.get_style(title_text)
            except MissingStyle:
                title_text = Text(self.title, style=self.style)
        else:
            if self.gradient_title:
                title_text = Gradient(self.title, bold=True).as_text()
            else:
                title_text = Text(self.title, style=self.style)

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

            center_index = randint(0, 9)
            center_color = NamedColor(center_index)
            left_index = center_index - 2
            if left_index < 0:
                left_index += 10
            left_color = NamedColor(left_index)
            right_index = center_index + 2
            if right_index > 9:
                right_index -= 10
            right_color = NamedColor(right_index)
            left_str = characters * (side_width // chars_len + 1)
            if not self.thick:
                left = Gradient(left_str, left_color, center_color, bold=True).as_text()
            else:
                left = Gradient(
                    left_str, left_color, center_color, color_box=True
                ).as_text()
            left.truncate(side_width - 1)
            right_length = width - cell_len(left.plain) - cell_len(title_text.plain)
            right_str = characters * (side_width // chars_len + 1)
            if not self.thick:
                right = Gradient(
                    right_str, center_color, right_color, bold=True
                ).as_text()
            else:
                right = Gradient(
                    right_str, center_color, right_color, color_box=True, bold=True
                ).as_text()
            right.truncate(right_length)
            rule_text.append_text(left)
            if self.thick:
                space = Text(" ", style=f"style.{center_color}")
                title_text.stylize(f"style.{center_color}")
                rule_text.append_text(space)
                rule_text.append_text(title_text)
                rule_text.append_text(space)
            else:
                rule_text.append_text(Text(" "))
                rule_text.append_text(title_text)
                rule_text.append_text(Text(" "))
            rule_text.append_text(right)
            rule_text.truncate(width)
        elif self.align == "left":
            _start_index = randint(0, 9)
            _start_color = NamedColor(_start_index)
            title_text.truncate(truncate_width, overflow="ellipsis")
            rule_str = characters * ((width - rule_text.cell_len) + 2)
            if self.thick:
                title_text.stylize(f"style.{_start_color}")
                rule_text.append(title_text)
                rule_text.append(Text(" ", style=f"style.{_start_color}"))
                rule = Gradient(
                    rule_str, start=_start_color, color_box=True, bold=True
                ).as_text()
                rule_text.append(rule)
                rule_text.truncate(width)
            else:
                rule_text.append(title_text)
                rule_text.append(" ")
                rule = Gradient(rule_str, bold=True).as_text()
                rule_text.append(rule)
                rule_text.truncate(width)
        elif self.align == "right":
            _start_index = randint(0, 9)
            _start_color = NamedColor(_start_index)
            _end_index = _start_index + 2
            if _end_index > 9:
                _end_index -= 10
            _end_color = NamedColor(_end_index)
            title_text.truncate(truncate_width, overflow="ellipsis")
            rule_str = characters * (width - title_text.cell_len - 1)
            if self.thick:
                title_text.stylize(f"style.{_end_color}")
                space = Text(" ", style=f"style.{_end_color}")
                rule = Gradient(
                    rule_str,
                    start=_start_color,
                    end=_end_color,
                    color_box=True,
                    bold=True,
                ).as_text()
                rule_text.append(rule)
                rule_text.append(space)
                rule_text.append(title_text)
            else:
                space = Text(" ")
                rule = Gradient(rule_str, bold=True).as_text()
                rule_text.append(rule)
                rule_text.append(space)
                rule_text.append(title_text)

        rule_text.plain = set_cell_size(rule_text.plain, width)
        return rule_text

    def _rule_line(self, chars_len: int, width: int) -> Text:
        rule_str = self.characters * ((width // chars_len) + 3)
        if not self.thick:
            rule_text = Gradient(rule_str, bold=True).as_text()
        else:
            rule_text = Gradient(rule_str, color_box=True).as_text()
        rule_text.truncate(width)
        rule_text.plain = set_cell_size(rule_text.plain, width)
        return rule_text


if __name__ == "__main__":  # pragma: no cover
    import sys

    from max.console import MaxConsole  # pylint: disable=reimported

    try:
        TEXT1 = sys.argv[1]
        TEXT2 = sys.argv[1]
        TEXT3 = sys.argv[1]
    except IndexError:
        TEXT1 = "Underlined Gradient Rule"
        TEXT2 = "Gradient Title on Left"
        TEXT3 = "Regular Title on Right"
    console = MaxConsole()
    rule1 = GradientRule(title=TEXT1, style="underline white")
    console.print(rule1)

    rule2 = GradientRule(
        title=TEXT2, gradient_title=True, style="underline", align="left"
    )
    console.print(rule2)

    rule3 = GradientRule(title=TEXT3, align="right")
    console.print(rule3)

    console.print(GradientRule())
    console.line(2)

    # Thick Gradient Rules
    console.print(GradientRule(title="Or thicker if you prefer!", thick=True))
    console.line()
    console.print(
        GradientRule(title="Without sacrificing...", align="left", thick=True)
    )
    console.line()
    console.print(GradientRule(title="...any finesse!", align="right", thick=True))
    console.line(2)
