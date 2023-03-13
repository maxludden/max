"""This module generates a custom theme for the other modules of Max."""
# pylint: disable=unused-import
from pathlib import Path
from typing import Dict, Mapping, Optional

import toml
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
    "bold.black": Style(color="#000000", bold=True),
    "dark_gray": Style(color="#444444"),
    "bold.dark_gray": Style(color="#444444", bold=True),
    "grey": Style(color="#888888"),
    "bold.grey": Style(color="#888888", bold=True),
    "light_gray": Style(color="#cccccc"),
    "bold.light_gray": Style(color="#cccccc", bold=True),
    "white": Style(color="#ffffff"),
    "bold.white": Style(color="#ffffff", bold=True),
    "red": Style(color="#ff0000"),
    "bold.red": Style(color="#ff0000", bold=True),
    "orange": Style(color="#ff8800"),
    "bold.orange": Style(color="#ff8800", bold=True),
    "yellow": Style(color="#ffff00"),
    "bold.yellow": Style(color="#ffff00", bold=True),
    "green": Style(color="#00ff00"),
    "bold.green": Style(color="#00ff00", bold=True),
    "cyan": Style(color="#00ffff"),
    "bold.cyan": Style(color="#00ffff", bold=True),
    "light_blue": Style(color="#0088ff"),
    "bold.light_blue": Style(color="#0088ff", bold=True),
    "blue": Style(color="#0000ff"),
    "bold.blue": Style(color="#0000ff", bold=True),
    "purple": Style(color="#5f00ff"),
    "bold.purple": Style(color="#5f00ff", bold=True),
    "light_purple": Style(color="#af00ff"),
    "bold.light_purple": Style(color="#af00ff", bold=True),
    "magenta": Style(color="#ff00ff"),
    "bold.magenta": Style(color="#ff00ff", bold=True),
    "cs.red": Style(color="#ff0000", bgcolor="#ff0000"),
    "cs.orange": Style(color="#ff8800", bgcolor="#ff8800"),
    "cs.yellow": Style(color="#ffff00", bgcolor="#ffff00"),
    "cs.green": Style(color="#00ff00", bgcolor="#00ff00"),
    "cs.cyan": Style(color="#00ffff", bgcolor="#00ffff"),
    "cs.light_blue": Style(color="#0088ff", bgcolor="#0088ff"),
    "cs.blue": Style(color="#0000ff", bgcolor="#0000ff"),
    "cs.purple": Style(color="#5f00ff", bgcolor="#5f00ff"),
    "cs.light_purple": Style(color="#af00ff", bgcolor="#af00ff"),
    "cs.magenta": Style(color="#ff00ff", bgcolor="#ff00ff"),
    "style.red": Style(color="#ffffff", bgcolor="#ff0000", bold=True),
    "style.orange": Style(color="#000000", bgcolor="#ff8800", bold=True),
    "style.yellow": Style(color="#000000", bgcolor="#ffff00", bold=True),
    "style.green": Style(color="#000000", bgcolor="#00ff00", bold=True),
    "style.cyan": Style(color="#000000", bgcolor="#00ffff", bold=True),
    "style.light_blue": Style(color="#ffffff", bgcolor="#0088ff", bold=True),
    "style.blue": Style(color="#ffffff", bgcolor="#0000ff", bold=True),
    "style.light_purple": Style(color="#ffffff", bgcolor="#af00ff", bold=True),
    "style.purple": Style(color="#ffffff", bgcolor="#5f00ff", bold=True),
    "style.magenta": Style(color="#000000", bgcolor="#ff00ff", bold=True),
    "inspect.attr": Style(color="#ffff00", italic=True),
    "inspect.attr.dunder": Style(color="#ffff00", italic=True, dim=True),
    "inspect.callable": Style(bold=True, color="#ff0000"),
    "inspect.async_def": Style(italic=True, color="#00ffff"),
    "inspect.def": Style(italic=True, color="#00ffff"),
    "inspect.class": Style(italic=True, color="#00ffff"),
    "inspect.error": Style(bold=True, color="#ff0000"),
    "inspect.equals": Style(),
    "inspect.help": Style(color="#00ffff"),
    "inspect.doc": Style(dim=True),
    "inspect.value.border": Style(color="#00ff00"),
    "live.ellipsis": Style(bold=True, color="#ff0000"),
    "layout.tree.row": Style(dim=False, color="#ff0000"),
    "layout.tree.column": Style(dim=False, color="#0000ff"),
    "logging.keyword": Style(bold=True, color="#ffff00"),
    "logging.level.notset": Style(dim=True),
    "logging.level.debug": Style(color="#0088ff"),
    "logging.level.info": Style(color="#ff00ff"),
    "logging.level.success": Style(color="#00ff00", bold=True),
    "logging.level.warning": Style(color="#ff0000"),
    "logging.level.error": Style(color="#ff0000", bold=True),
    "logging.level.critical": Style(color="#ff0000", bold=True, reverse=True),
    "log.level": Style.null(),
    "log.time": Style(color="#00ffff", dim=True),
    "log.message": Style.null(),
    "log.path": Style(dim=True),
    "repr.ellipsis": Style(color="#ffff00"),
    "repr.indent": Style(color="#00ff00", dim=True),
    "repr.error": Style(color="#ff0000", bold=True),
    "repr.str": Style(color="#00ff00", italic=False, bold=False),
    "repr.brace": Style(bold=True),
    "repr.comma": Style(bold=True),
    "repr.ipv4": Style(bold=True, color="#00ff00"),
    "repr.ipv6": Style(bold=True, color="#00ff00"),
    "repr.eui48": Style(bold=True, color="#00ff00"),
    "repr.eui64": Style(bold=True, color="#00ff00"),
    "repr.tag_start": Style(bold=True),
    "repr.tag_name": Style(color="#00ff00", bold=True),
    "repr.tag_contents": Style(color="default"),
    "repr.tag_end": Style(bold=True),
    "repr.attrib_name": Style(color="#ffff00", italic=False),
    "repr.attrib_equal": Style(bold=True),
    "repr.attrib_value": Style(color="#00ff00", italic=False),
    "repr.number": Style(color="#00ffff", bold=True, italic=False),
    "repr.number_complex": Style(color="#00ffff", bold=True, italic=False),  # same
    "repr.bool_true": Style(color="#00ff00", italic=True),
    "repr.bool_false": Style(color="#ff0000", italic=True),
    "repr.none": Style(color="#00ff00", italic=True),
    "repr.url": Style(underline=True, color="#0000ff", italic=False, bold=False),
    "repr.uuid": Style(color="#ffff00", bold=False),
    "repr.call": Style(color="#00ff00", bold=True),
    "repr.path": Style(color="#00ff00"),
    "repr.filename": Style(color="#00ff00"),
    "rule.line": Style(color="#00ff00"),
    "rule.text": Style(color="#ffffff", bold=True),
    "json.brace": Style(bold=True),
    "json.bool_true": Style(color="#00ff00", italic=True),
    "json.bool_false": Style(color="#ff0000", italic=True),
    "json.null": Style(color="#00ff00", italic=True),
    "json.number": Style(color="#00ffff", bold=True, italic=False),
    "json.str": Style(color="#00ff00", italic=False, bold=False),
    "json.key": Style(color="#0000ff", bold=True),
    "prompt": Style.null(),
    "prompt.choices": Style(color="#ff00ff", bold=True),
    "prompt.default": Style(color="#00ffff", bold=True),
    "prompt.invalid": Style(color="#ff0000"),
    "prompt.invalid.choice": Style(color="#ff0000"),
    "pretty": Style.null(),
    "scope.border": Style(color="#0000ff"),
    "scope.key": Style(color="#ffff00", italic=True),
    "scope.key.special": Style(color="#ffff00", italic=True, dim=True),
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
    "markdown.code": Style(bold=True, color="#00ffff", bgcolor="black"),
    "markdown.code_block": Style(color="#00ffff", bgcolor="black"),
    "markdown.block_quote": Style(color="#00ff00"),
    "markdown.list": Style(color="#00ffff"),
    "markdown.item": Style(),
    "markdown.item.bullet": Style(color="#ffff00", bold=True),
    "markdown.item.number": Style(color="#ffff00", bold=True),
    "markdown.hr": Style(color="#ffffff"),
    "markdown.h1.border": Style(),
    "markdown.h1": Style(bold=True),
    "markdown.h2": Style(bold=True, underline=True),
    "markdown.h3": Style(bold=True),
    "markdown.h4": Style(bold=True, dim=True),
    "markdown.h5": Style(underline=True),
    "markdown.h6": Style(italic=True),
    "markdown.h7": Style(italic=True, dim=True),
    "markdown.link": Style(color="#0000ff"),
    "markdown.link_url": Style(color="#0000ff", underline=True),
    "markdown.s": Style(strike=True),
    "iso8601.date": Style(color="#0000ff"),
    "iso8601.time": Style(color="#ff00ff"),
    "iso8601.timezone": Style(color="#ffff00"),
}
path = Path("/Users/maxludden/dev/py/max/static/_max_theme.json")
# with open(path, mode="wt", encoding="utf-8") as file:
#     dump(dict(MAX_STYLES), file)


class MaxTheme(Theme):
    """A container for style information, used by :class:'max.max.MaxConsole'.
    Args:
        styles (Dict[str, Style], optional): A mapping of style names on to \
            styles. Defaults to None for a theme with no styles.
        inherit (bool, optional): Inherit default styles. Defaults to True.wo
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

    table = Table("Name", "Styling", "New")

    for style_name, style in MAX_STYLES.items():
        table.add_row(Text(style_name, style=style), str(style))

    console.print(table)
    if html:
        print(console.export_html(inline_styles=True))

    new_styles = {
        "red": Style(color="#ff0000"),
        "bold.red": Style(color="#ff0000", bold=True),
        "cs.red": Style(color="#ff0000", bgcolor="#ff0000"),
        "style.red": Style(color="#ffffff", bgcolor="#ff0000"),
        "orange": Style(color="#ff8800"),
        "bold.orange": Style(color="#ff8800", bold=True),
        "cs.orange": Style(color="#ff8800", bgcolor="#ff8800"),
        "style.orange": Style(color="#000000", bgcolor="#ff8800"),
        "yellow": Style(color="#ffff00"),
        "bold.yellow": Style(color="#ffff00", bold=True),
        "cs.yellow": Style(color="#ffff00", bgcolor="#ffff00"),
        "style.yellow": Style(color="#000000", bgcolor="#ffff00"),
        "green": Style(color="#00ff00"),
        "bold.green": Style(color="#00ff00", bold=True),
        "cs.green": Style(color="#00ff00", bgcolor="#00ff00"),
        "style.green": Style(color="#000000", bgcolor="#00ff00"),
        "cyan": Style(color="#00ffff"),
        "bold.cyan": Style(color="#00ffff", bold=True),
        "cs.cyan": Style(color="#00ffff", bgcolor="#00ffff"),
        "style.cyan": Style(color="#000000", bgcolor="#00ffff"),
        "light_blue": Style(color="#0088ff"),
        "bold.light_blue": Style(color="#0088ff", bold=True),
        "cs.light_blue": Style(color="#0088ff", bgcolor="#0088ff"),
        "style.light_blue": Style(color="#ffffff", bgcolor="#0088ff"),
        "blue": Style(color="#0000ff"),
        "bold.blue": Style(color="#0000ff", bold=True),
        "cs.blue": Style(color="#0000ff", bgcolor="#0000ff"),
        "style.blue": Style(color="#ffffff", bgcolor="#0000ff"),
        "purple": Style(color="#5f00ff"),
        "bold.purple": Style(color="#5f00ff", bold=True),
        "cs.purple": Style(color="#5f00ff", bgcolor="#5f00ff"),
        "style.purple": Style(color="#ffffff", bgcolor="#5f00ff"),
        "light_purple": Style(color="#af00ff"),
        "bold.light_purple": Style(color="#af00ff", bold=True),
        "cs.light_purple": Style(color="#af00ff", bgcolor="#af00ff"),
        "style.light_purple": Style(color="#ffffff", bgcolor="#af00ff"),
        "magenta": Style(color="#ff00ff"),
        "bold.magenta": Style(color="#ff00ff", bold=True),
        "cs.magenta": Style(color="#ff00ff", bgcolor="#ff00ff"),
        "style.magenta": Style(color="#000000", bgcolor="#ff00ff"),
    }

    table2 = Table(
        "Name",
        "Styling",
        title="\n\n :star: New Styles :star:",
        title_style="bold italic #ff00ff",
        width=115,
    )

    for style_name, style in new_styles.items():
        table2.add_row(Text(style_name, style=style), str(style))

    console.print(table2)
    if html:
        print(console.export_html(inline_styles=True))

with open(Path.cwd() / "static" / "max_theme.toml", "wt", encoding="ufc-8") as file:
    toml.dump(MAX_STYLES, file)
