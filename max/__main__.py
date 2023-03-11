"""Import max modules."""
# pylint: disable=unused-import, unused-argument
from typing import Optional

from rich.align import AlignMethod
from rich.cells import cell_len, set_cell_size
from rich.jupyter import JupyterMixin
from rich.measure import Measurement
from rich.panel import Panel
from rich.style import Style
from rich.text import Text

from max.color_index import ColorIndex
from max.console import BaseMaxConsole
from max.console import BaseMaxConsole as Console
from max.console import (
    ConsoleOptions,
    JustifyMethod,
    OverflowMethod,
    RenderResult,
    Singleton,
    install_traceback,
)
from max.gradient import Gradient
from max.named_color import NamedColor
from max.progress import MaxProgress
from max.theme import MaxTheme, Theme

DEFAULT_JUSTIFY: "JustifyMethod" = "default"
DEFAULT_OVERFLOW: "OverflowMethod" = "fold"


class MaxConsole(BaseMaxConsole, metaclass=Singleton):
    """A custom themed high level interface for the MaxConsole class that \
        inherits from max.BaseMaxConsole which inherits from rich.console.Console.

    Args:
        color_system (str, optional): The color system supported \
            by your terminal, either "standard", "256" or \
            "truecolor". Leave as "auto" to autodetect.
        force_terminal (Optional[bool], optional): Enable/disable terminal \
            control codes, or None to auto-detect terminal. Defaults to None.
        force_jupyter (Optional[bool], optional): Enable/disable Jupyter \
            rendering, or None to auto-detect Jupyter. Defaults to None.
        force_interactive (Optional[bool], optional): Enable/disable \
            interactive mode, or None to auto detect. Defaults to None.
        soft_wrap (Optional[bool], optional): Set soft wrap default on \
            print method. Defaults to False.
        theme (Theme, optional): An optional style theme object, or \
            None for max's default theme.
        stderr (bool, optional): Use stderr rather than stdout if \
            file is not specified. Defaults to False.
        file (IO, optional): A file object where the console \
            should write to. Defaults to stdout.
        quiet (bool, Optional): Boolean to suppress all output. \
            Defaults to False.
        width (int, optional): The width of the terminal. Leave \
            as default to auto-detect width.
        height (int, optional): The height of the terminal. Leave \
            as default to auto-detect height.
        style (StyleType, optional): Style to apply to all output, \
            or None for no style. Defaults to None.
        no_color (Optional[bool], optional): Enabled no color \
            mode, or None to auto detect. Defaults to None.
        tab_size (int, optional): Number of spaces used to replace \
            a tab character. Defaults to 8.
        record (bool, optional): Boolean to enable recording of \
            terminal output,
                required to call export_html, export_svg, and \
                    export_text. Defaults to False.
        markup (bool, optional): Boolean to enable console_markup. \
            Defaults to True.
        emoji (bool, optional): Enable emoji code. Defaults to True.
        emoji_variant (str, optional): Optional emoji variant, either \
            "text" or "emoji". Defaults to None.
        highlight (bool, optional): Enable automatic highlighting. \
            Defaults to True.
        log_time (bool, optional): Boolean to enable logging of time \
            by log methods. Defaults to True.
        log_path (bool, optional): Boolean to enable the logging \
            of the caller by log. Defaults to True.
        log_time_format (Union[str, TimeFormatterCallable], optional): \
            If log_time is enabled, either string for strftime or \
                callable that formats the time. Defaults to "[%X] ".
        highlighter (HighlighterType, optional): Default highlighter.
        legacy_windows (bool, optional): Enable legacy Windows \
            mode, or None to auto detect. Defaults to None.
        safe_box (bool, optional): Restrict box options that \
            don't render on legacy Windows.
        get_datetime (Callable[[], datetime], optional): Callable \
            that gets the current time as a datetime.datetime object (used by Console.log),
            or None for datetime.now.
        get_time (Callable[[], time], optional): Callable that \
            gets the current time in seconds, default uses time.monotonic.
    """

    theme: Theme = MaxTheme()

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            theme=self.theme,
        )
        install_traceback(console=self)

    def gradient(  # pylint: disable=too-many-arguments
        text: str | Text,
        start: Optional[NamedColor | str | int] = None,
        end: Optional[NamedColor | str | int] = None,
        justify: JustifyMethod = DEFAULT_JUSTIFY,
        invert: bool = False,
        length: int = 3,
        console: Console = Console(),  # pylint: disable=W0621:redefined-outer-name
        overflow: OverflowMethod = DEFAULT_OVERFLOW,
        title: str = "Gradient",
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
            verbose=verbose,
        )

    def gradient_rule(
        self,
        start: Optional[NamedColor | str | int] = None,
        end: Optional[NamedColor | str | int] = None,
        invert: bool = False,
        length: int = 3,
        console: Console = Console(),  # pylint: disable=W0621:redefined-outer-name
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
