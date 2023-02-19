"""MaxConsole is a custom themed class inheriting from rich.console.Console."""
# pylint: disable=unused-import
import threading
from dataclasses import dataclass

from rich import inspect
from rich.console import (
    Console,
    ConsoleRenderable,
    RichCast,
    ConsoleOptions,
    RenderResult
)
from rich.theme import Theme
from rich.text import Text
from rich.traceback import install as install_traceback

from max.theme import MaxTheme

RenderableType = ConsoleRenderable | RichCast | str


def singleton(cls):
    """Singleton decorator for MaxConsole."""
    instance = None
    lock = threading.Lock()

    def get_instance(*args, **kwargs):
        nonlocal instance
        if instance is None:
            with lock:
                if instance is None:
                    instance = cls(*args, **kwargs)
        return instance

    return get_instance


@dataclass
class MaxConsole(Console):
    """A custom themed high level interface for the MaxConsole class that \
        inherits from rich.console.Console

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
        super().__init__(*args, **kwargs, theme=self.theme, )
        install_traceback(console=self)
        

    @staticmethod
    def colorful_hello():
        """Print 'Hello World' in a colorful manner"""
        return "[bold #ff0000]H[/][bold #ff8800]e[/][bold #ffff00]l[/][bold \
            #00ff00]l[/][bold #00ffff]o[/][bold #0088ff] W[/][bold \
            #0000ff]o[/][bold #5f00ff]r[/][bold #af00ff]l[/][bold \
            #ff00ff]d[/][bold #ff0000]![/]"

if __name__ == "__main__":
    console = MaxConsole()
    console.clear()
    console.line(2)
    console.print(console.colorful_hello(), justify='center', width=115)

    EXPLANATION=[
        "\n\nMaxConsole is a custom themed class inheriting from ",
        "rich.console.Console. It is a global singleton class that can ",
        "be imported and used anywhere in the project and used as a ",
        "drop in replacement for rich.console.Console.\n\n"
    ]
    EXP = Text.assemble(*EXPLANATION)
    console.print(EXP, width=115, justify='left')

    inspect(console)
    