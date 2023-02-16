"""This module generates a custom theme for the other modules of Max."""

from typing import Dict, Optional, Mapping
from rich.style import Style, StyleType
from rich.theme import Theme

MAX_STYLES: Dict[str, Style] = {
    "none": Style.null(),
    "reset": Style(
        color="default",
        bgcolor="default",
        dim=False,
        bold=False,
        italic=False,
        underline=False,
        blink=False,
        blink2=False,
        reverse=False,
        conceal=False,
        strike=False,
    ),
    "dim": Style(dim=True),
    "bright": Style(dim=False),
    "bold": Style(bold=True),
    "strong": Style(bold=True),
    "code": Style(reverse=True, bold=True),
    "italic": Style(italic=True),
    "emphasize": Style(italic=True),
    "underline": Style(underline=True),
    "blink": Style(blink=True),
    "blink2": Style(blink2=True),
    "reverse": Style(reverse=True),
    "strike": Style(strike=True),
    "black": Style(color="#000000"),
    "dark_gray": Style(color="#444444"),
    "grey": Style(color="#888888"),
    "light_gray": Style(color="#cccccc"),
    "white": Style(color="#ffffff"),
    "red": Style(color="#ff0000"),
    "namedcolor.red": Style(color="#ff0000"),
    "orange": Style(color="#ff8800"),
    "namedcolor.orange": Style(color="#ff8800"),
    "yellow": Style(color="#ffff00"),
    "namedcolor.yellow": Style(color="#ffff00"),
    "green": Style(color="#00ff00"),
    "namedcolor.green": Style(color="#00ff00"),
    "cyan": Style(color="#00ffff"),
    "namedcolor.cyan": Style(color="#00ffff"),
    "light_blue": Style(color="#0088ff"),
    "namedcolor.light_blue": Style(color="#0088ff"),
    "blue": Style(color="#0000ff"),
    "namedcolor.blue": Style(color="#0000ff"),
    "purple": Style(color="#5f00ff"),
    "namedcolor.purple": Style(color="#5f00ff"),
    "light_purple": Style(color="#af00ff"),
    "namedcolor.light_purple": Style(color="#af00ff"),
    "magenta": Style(color="#ff00ff"),
    "namedcolor.magenta": Style(color="#ff00ff"),
    "inspect.attr": Style(color="yellow", italic=True),
    "inspect.attr.dunder": Style(color="yellow", italic=True, dim=True),
    "inspect.callable": Style(bold=True, color="#ff0000"),
    "inspect.async_def": Style(italic=True, color="bright_cyan"),
    "inspect.def": Style(italic=True, color="bright_cyan"),
    "inspect.class": Style(italic=True, color="bright_cyan"),
    "inspect.error": Style(bold=True, color="#ff0000"),
    "inspect.equals": Style(),
    "inspect.help": Style(color="cyan"),
    "inspect.doc": Style(dim=True),
    "inspect.value.border": Style(color="green"),
    "live.ellipsis": Style(bold=True, color="#ff0000"),
    "layout.tree.row": Style(dim=False, color="#ff0000"),
    "layout.tree.column": Style(dim=False, color="#0000ff"),
    "logging.keyword": Style(bold=True, color="yellow"),
    "logging.level.notset": Style(dim=True),
    "logging.level.debug": Style(color="#0088ff"),
    "logging.level.info": Style(color="#ff00ff"),
    "logging.level.warning": Style(color="#ff0000"),
    "logging.level.error": Style(color="#ff0000", bold=True),
    "logging.level.critical": Style(color="#ff0000", bold=True, reverse=True),
    "log.level": Style.null(),
    "log.time": Style(color="cyan", dim=True),
    "log.message": Style.null(),
    "log.path": Style(dim=True),
    "repr.ellipsis": Style(color="yellow"),
    "repr.indent": Style(color="green", dim=True),
    "repr.error": Style(color="#ff0000", bold=True),
    "repr.str": Style(color="green", italic=False, bold=False),
    "repr.brace": Style(bold=True),
    "repr.comma": Style(bold=True),
    "repr.ipv4": Style(bold=True, color="bright_green"),
    "repr.ipv6": Style(bold=True, color="bright_green"),
    "repr.eui48": Style(bold=True, color="bright_green"),
    "repr.eui64": Style(bold=True, color="bright_green"),
    "repr.tag_start": Style(bold=True),
    "repr.tag_name": Style(color="bright_magenta", bold=True),
    "repr.tag_contents": Style(color="default"),
    "repr.tag_end": Style(bold=True),
    "repr.attrib_name": Style(color="yellow", italic=False),
    "repr.attrib_equal": Style(bold=True),
    "repr.attrib_value": Style(color="magenta", italic=False),
    "repr.number": Style(color="cyan", bold=True, italic=False),
    "repr.number_complex": Style(color="cyan", bold=True, italic=False),  # same
    "repr.bool_true": Style(color="bright_green", italic=True),
    "repr.bool_false": Style(color="#ff0000", italic=True),
    "repr.none": Style(color="magenta", italic=True),
    "repr.url": Style(underline=True, color="bright_blue", italic=False, bold=False),
    "repr.uuid": Style(color="bright_yellow", bold=False),
    "repr.call": Style(color="magenta", bold=True),
    "repr.path": Style(color="magenta"),
    "repr.filename": Style(color="bright_magenta"),
    "rule.line": Style(color="bright_green"),
    "rule.text": Style.null(),
    "json.brace": Style(bold=True),
    "json.bool_true": Style(color="bright_green", italic=True),
    "json.bool_false": Style(color="#ff0000", italic=True),
    "json.null": Style(color="magenta", italic=True),
    "json.number": Style(color="cyan", bold=True, italic=False),
    "json.str": Style(color="green", italic=False, bold=False),
    "json.key": Style(color="#0000ff", bold=True),
    "prompt": Style.null(),
    "prompt.choices": Style(color="#ff00ff", bold=True),
    "prompt.default": Style(color="#00ffff", bold=True),
    "prompt.invalid": Style(color="#ff0000"),
    "prompt.invalid.choice": Style(color="#ff0000"),
    "pretty": Style.null(),
    "scope.border": Style(color="#0000ff"),
    "scope.key": Style(color="yellow", italic=True),
    "scope.key.special": Style(color="yellow", italic=True, dim=True),
    "scope.equals": Style(color="#ff0000"),
    "table.header": Style(bold=True),
    "table.footer": Style(bold=True),
    "table.cell": Style.null(),
    "table.title": Style(italic=True),
    "table.caption": Style(italic=True, dim=True),
    "traceback.error": Style(color="#ff0000", italic=True),
    "traceback.border.syntax_error": Style(color="#ff0000"),
    "traceback.border": Style(color="#ff0000"),
    "traceback.text": Style.null(),
    "traceback.title": Style(color="#ff0000", bold=True),
    "traceback.exc_type": Style(color="#ff0000", bold=True),
    "traceback.exc_value": Style.null(),
    "traceback.offset": Style(color="#ff0000", bold=True),
    "bar.back": Style(color="grey23"),
    "bar.complete": Style(color="#646464"),
    "bar.finished": Style(color="#006a20"),
    "bar.pulse": Style(color="#f92672"),
    "progress.description": Style.null(),
    "progress.filesize": Style(color="#00ff00"),
    "progress.filesize.total": Style(color="#00ff00"),
    "progress.download": Style(color="#00ff00"),
    "progress.elapsed": Style(color="#ffff00"),
    "progress.percentage": Style(color="#ff00ff"),
    "progress.remaining": Style(color="#00ffff"),
    "progress.data.speed": Style(color="#ff0000"),
    "progress.spinner": Style(color="#00ff00"),
    "status.spinner": Style(color="#00ff00"),
    "tree": Style(),
    "tree.line": Style(),
    "markdown.paragraph": Style(),
    "markdown.text": Style(),
    "markdown.em": Style(italic=True),
    "markdown.emph": Style(italic=True),  # For commonmark backwards compatibility
    "markdown.strong": Style(bold=True),
    "markdown.code": Style(bold=True, color="cyan", bgcolor="black"),
    "markdown.code_block": Style(color="cyan", bgcolor="black"),
    "markdown.block_quote": Style(color="magenta"),
    "markdown.list": Style(color="cyan"),
    "markdown.item": Style(),
    "markdown.item.bullet": Style(color="yellow", bold=True),
    "markdown.item.number": Style(color="yellow", bold=True),
    "markdown.hr": Style(color="#ffffff"),
    "markdown.h1.border": Style(),
    "markdown.h1": Style(bold=True),
    "markdown.h2": Style(bold=True, underline=True),
    "markdown.h3": Style(bold=True),
    "markdown.h4": Style(bold=True, dim=True),
    "markdown.h5": Style(underline=True),
    "markdown.h6": Style(italic=True),
    "markdown.h7": Style(italic=True, dim=True),
    "markdown.link": Style(color="bright_blue"),
    "markdown.link_url": Style(color="#0000ff", underline=True),
    "markdown.s": Style(strike=True),
    "iso8601.date": Style(color="#0000ff"),
    "iso8601.time": Style(color="#ff00ff"),
    "iso8601.timezone": Style(color="#ffff00"),
}


class MaxTheme(Theme):
    """A container for style information, used by :class:'max.console.MaxConsole'.
    Args:
        styles (Dict[str, Style], optional): A mapping of style names on to \
            styles. Defaults to None for a theme with no styles.
        inherit (bool, optional): Inherit default styles. Defaults to True.
    """

    styles: Dict[str, Style]

    def __init__(
        self, styles: Optional[Mapping[str, StyleType]] = None, inherit: bool = True
    ):
        super().__init__(styles=styles, inherit=True)
        self.styles = MAX_STYLES.copy() if inherit else {}
        if styles is not None:
            self.styles.update(
                {
                    name: style if isinstance(style, Style) else Style.parse(style)
                    for name, style in styles.items()
                }
            )


if __name__ == "__main__":  # pragma: no cover
    import argparse
    import io

    from rich.console import Console
    from rich.table import Table
    from rich.text import Text

    parser = argparse.ArgumentParser()
    parser.add_argument("--html", action="store_true", help="Export as HTML table")
    args = parser.parse_args()
    html: bool = args.html
    console = Console(record=True, width=70, file=io.StringIO()) if html else Console()

    table = Table("Name", "Styling")

    for style_name, style in MAX_STYLES.items():
        table.add_row(Text(style_name, style=style), str(style))

    console.print(table)
    if html:
        print(console.export_html(inline_styles=True))
        