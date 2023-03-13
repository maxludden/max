from pathlib import Path
from typing import Dict, Optional, Mapping
import toml

from rich.theme import Theme
from rich.style import Style, StyleType


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
max_styles_path = Path.cwd()/ "static" / "maxtheme.toml"
with open (max_styles_path, "r") as f:
    