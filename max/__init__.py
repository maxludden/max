"""Import max modules."""
# pylint: disable=unused-import, unused-argument, invalid-name, global-statement/
# pylint: disable=redefined-outer-name
from typing import Optional, Self

from rich.align import AlignMethod
from rich.cells import cell_len, set_cell_size
from rich.console import JustifyMethod, OverflowMethod
from rich.text import Text

from max.console import MaxConsole
from max.gradient import Gradient
from max.named_color import NamedColor

DEFAULT_JUSTIFY: "JustifyMethod" = "default"
DEFAULT_OVERFLOW: "OverflowMethod" = "fold"


def __call__(self, *args, **kwargs):
    return MaxConsole(*args, **kwargs)


def gradient(  # pylint: disable=too-many-arguments
    self,
    text: str | Text,
    start: Optional[NamedColor | str | int] = None,
    end: Optional[NamedColor | str | int] = None,
    justify: JustifyMethod = DEFAULT_JUSTIFY,
    invert: bool = False,
    length: int = 3,
    console: MaxConsole = MaxConsole(),
    overflow: OverflowMethod = DEFAULT_OVERFLOW,
    title: str = "Gradient",
    bold: bool = False,
    rainbow: bool = False,
    verbose: bool = False,
) -> Text:
    """Create gradient text.

    Args:
        text (str|Text): The text to apply the gradient to.
        start (Optional[NamedColor | str | int], optional): The start color of the \
            gradient. Defaults to None.
        end (Optional[NamedColor | str | int], optional): The end color of the \
            gradient. Defaults to None.
        justify (JustifyMethod, optional): The justification of the text. \
            Defaults to DEFAULT_JUSTIFY.
        invert (bool, optional): Invert the gradient. Defaults to False.
        length (int, optional): The length of the gradient. Defaults to 3.
        console (MaxConsole, optional): The console to use. Defaults to \
            MaxConsole().
        overflow (OverflowMethod, optional): The overflow method. Defaults \
            to DEFAULT_OVERFLOW.
        title (str, optional): The title of the gradient. Defaults to \
            "Gradient".
        verbose (bool, optional): Print verbose output. Defaults to False."""
    if isinstance(text, Text):
        text = str(text)
    if isinstance(start, int):
        start = NamedColor.colors[start]
    if isinstance(end, int):
        end = NamedColor.colors[end]

    return Gradient(
        text=text,
        start=start,
        end=end,
        justify=justify,
        invert=invert,
        length=length,
        console=console,
        overflow=overflow,
        title=title,
        bold=bold,
        rainbow=rainbow,
        verbose=verbose,
    )


def gradient_rule(
    self,
    start: Optional[NamedColor | str | int] = None,
    end: Optional[NamedColor | str | int] = None,
    invert: bool = False,
    length: int = 3,
    console: MaxConsole = MaxConsole(),
    title: str = "Gradient",
    verbose: bool = False,
) -> Text:
    """Create gradient rule.

    Args:
        start (Optional[NamedColor | str | int], optional): The start color of the \
            gradient. Defaults to None.
        end (Optional[NamedColor | str | int], optional): The end color of the \
            gradient. Defaults to None.
        invert (bool, optional): Invert the gradient. Defaults to False.
        length (int, optional): The length of the gradient. Defaults to 3.
        console (MaxConsole, optional): The console to use. Defaults to \
            MaxConsole().
        title (str, optional): The title of the gradient. Defaults to \
            "Gradient".
        verbose (bool, optional): Print verbose output. Defaults to False."""
    return self.gradient(
        text="",
        start=start,
        end=end,
        justify="left",
        invert=invert,
        length=length,
        console=console,
        overflow="fold",
        title=title,
        verbose=verbose,
    )


def get_console() -> MaxConsole:
    """Get a global :class:`~max.MaxConsole` instance. This function is used when Max requires/
        a console and hasn't been explicitly given one.

    Returns:
        MaxConsole: a MaxConsole instance.
    """
    global _console  # pylint: disable=global-variable-undefined
    if _console is None:
        _console = MaxConsole()
    return _console
