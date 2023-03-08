"""Import max modules."""
# pylint: disable=unused-import
from typing import Optional

from rich.align import AlignMethod
from rich.cells import cell_len, set_cell_size
from rich.jupyter import JupyterMixin
from rich.measure import Measurement
from rich.panel import Panel
from rich.style import Style
from rich.text import Text

from max.color_index import ColorIndex
from max.console import (
    ConsoleOptions,
    JustifyMethod,
    MaxConsole,
    OverflowMethod,
    RenderResult,
)
from max.gradient import Gradient
from max.named_color import NamedColor
from max.progress import MaxProgress
from max.theme import MaxTheme

DEFAULT_JUSTIFY: "JustifyMethod" = "default"
DEFAULT_OVERFLOW: "OverflowMethod" = "fold"


def gradient(
    text: str | Text,
    start: Optional[NamedColor | str | int] = None,
    end: Optional[NamedColor | str | int] = None,
    justify: Optional[JustifyMethod] = DEFAULT_JUSTIFY,
    invert: Optional[bool] = False,
    length: Optional[int] = 3,
    console: MaxConsole = MaxConsole(),  # pylint: disable=W0621:redefined-outer-name
    overflow: Optional[OverflowMethod] = DEFAULT_OVERFLOW,
    title: Optional[str] = "Gradient",
    verbose: Optional[bool] = False,
) -> Text:
    """Create gradient text.

    Args:
        text (str|Text): The text to apply the gradient to.
        start (Optional[NamedColor | str | int], optional): The start color of the \
gradient. Defaults to None.
        end (Optional[NamedColor | str | int], optional): The end color of the \
gradient. Defaults to None.
        justify (Optional[JustifyMethod], optional): The justification of the text. \
Defaults to DEFAULT_JUSTIFY.
        invert (Optional[bool], optional): Invert the gradient. Defaults to False.
        length (Optional[int], optional): The length of the gradient. Defaults to 3.
        console (MaxConsole, optional): The console to use. Defaults to \
MaxConsole().
        overflow (Optional[OverflowMethod], optional): The overflow method. Defaults \
to DEFAULT_OVERFLOW.
        title (Optional[str], optional): The title of the gradient. Defaults to \
"Gradient".
        verbose (Optional[bool], optional): Print verbose output. Defaults to False."""
    if isinstance(text, Text):
        text = str(text)

    indexes = []
    colors = []
