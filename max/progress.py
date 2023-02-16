from threading import Event, RLock, Thread
from typing import (
    Any,
    BinaryIO,
    Callable,
    ContextManager,
    Deque,
    Dict,
    Generic,
    Iterable,
    List,
    NamedTuple,
    NewType,
    Optional,
    Sequence,
    TextIO,
    Tuple,
    Type,
    TypeVar,
    Union,
)
from max.console import MaxConsole
from rich.console import Console
from rich.progress import (
    Progress,
    BarColumn,
    MofNCompleteColumn,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    Task,
    ProgressSample,
    ProgressColumn,
    TaskProgressColumn,
)
from rich.table import Column, Table
from rich.style import Style, StyleType, StyleStack
from rich.text import Text, Span, TextType
from rich import filesize, get_console
from rich.console import Console, Group, JustifyMethod, RenderableType
from rich.highlighter import Highlighter
from rich.jupyter import JupyterMixin
from rich.live import Live
from rich.progress_bar import ProgressBar
from rich.spinner import Spinner
from rich.text import Text, TextType
import time

TaskID = NewType("TaskID", int)

ProgressType = TypeVar("ProgressType")

GetTimeCallable = Callable[[], float]


class MaxProgress(Progress):
    """Renders an auto-updating progress bar(s).
    Args:
        console (Console, optional): Optional Console instance. Default will an internal Console instance writing to stdout.
        auto_refresh (bool, optional): Enable auto refresh. If disabled, you will need to call `refresh()`.
        refresh_per_second (Optional[float], optional): Number of times per second to refresh the progress information or None to use default (10). Defaults to None.
        speed_estimate_period: (float, optional): Period (in seconds) used to calculate the speed estimate. Defaults to 30.
        transient: (bool, optional): Clear the progress on exit. Defaults to False.
        redirect_stdout: (bool, optional): Enable redirection of stdout, so ``print`` may be used. Defaults to True.
        redirect_stderr: (bool, optional): Enable redirection of stderr. Defaults to True.
        get_time: (Callable, optional): A callable that gets the current time, or None to use Console.get_time. Defaults to None.
        disable (bool, optional): Disable progress display. Defaults to False
        expand (bool, optional): Expand tasks table to fit width. Defaults to False.
    """

    def __init__(
        self,
        *columns: Union[str, Progress, Column],
        console: Optional[MaxConsole] = None,
        auto_refresh: bool = True,
        refresh_per_second: float = 10,
        speed_estimate_period: float = 30.0,
        transient: bool = False,
        redirect_stdout: bool = True,
        redirect_stderr: bool = True,
        get_time: Optional[GetTimeCallable] = None,
        disable: bool = False,
        expand: bool = False,
    ) -> None:
        super().__init__(
            columns=columns or self.get_max_columns(),
            console=console or MaxConsole.get_console(),
            auto_refresh=auto_refresh,
            refresh_per_second=refresh_per_second,
            speed_estimate_period=speed_estimate_period,
            transient=transient,
            redirect_stdout=redirect_stdout,
            redirect_stderr=redirect_stderr,
            get_time=get_time,
            disable=disable,
            expand=expand,
        )
        self.columns = columns or self.get_max_columns()

    @classmethod
    def get_max_columns(cls) -> Tuple[ProgressColumn, ...]:
        """Get the default columns used for a new MaxProgress instance:
        - a text column for the description (TextColumn)
        - the bar itself (BarColumn)
        - a column showing the number of completed tasks (MofNCompleteColumn)
        - a column showing the elapsed time (TimeElapsedColumn)
        - an estimated-time-remaining column (TimeRemainingColumn)
        If the Progress instance is created without passing a columns argument,
        the default columns defined here will be used.
        You can also create a Progress instance using custom columns before
        and/or after the defaults, as in this example:
            progress = Progress(
                SpinnerColumn(),
                *Progress.default_columns(),
                "Elapsed:",
                TimeElapsedColumn(),
            )
        This code shows the creation of a Progress display, containing
        a spinner to the left, the default columns, and a labeled elapsed
        time column.
        """
        text_column = TextColumn("[progress.description]{task.description}")
        spinner_column = SpinnerColumn(
            spinner_name="point",
            style="#ff00ff",
            finished_text=Text("✓", style="#00ff00"),
            table_column=Column(),
        )
        bar_column = BarColumn(
            bar_width=None,  # Full width progress bar
            style=Style(color="#249df1"),  # While in-progress
            complete_style=Style(color="#00ff00"),  # Done
            finished_style=Style(color="#333333"),  # After completion
            table_column=Column(ratio=3),
        )
        mofn_column = MofNCompleteColumn()
        time_elapsed_column = TimeElapsedColumn()
        time_remaining_column = TimeRemainingColumn()
        return (
            text_column,
            spinner_column,
            bar_column,
            mofn_column,
            time_elapsed_column,
            time_remaining_column,
        )


if __name__ == "__main__":  # pragma: no coverage
    import random
    import time

    from rich.panel import Panel
    from rich.rule import Rule
    from rich.syntax import Syntax
    from rich.table import Table

    syntax = Syntax(
        '''def loop_last(values: Iterable[T]) -> Iterable[Tuple[bool, T]]:
    """Iterate and generate a tuple with a flag for last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    for value in iter_values:
        yield False, previous_value
        previous_value = value
    yield True, previous_value''',
        "python",
        line_numbers=True,
    )

    table = Table("foo", "bar", "baz")
    table.add_row("1", "2", "3")

    progress_renderables = [
        "Text may be printed while the progress bars are rendering.",
        Panel("In fact, [i]any[/i] renderable will work"),
        "Such as [magenta]tables[/]...",
        table,
        "Pretty printed structures...",
        {"type": "example", "text": "Pretty printed"},
        "Syntax...",
        syntax,
        Rule("Give it a try!"),
    ]

    from itertools import cycle

    examples = cycle(progress_renderables)

    console = Console(record=True)

    with Progress(
        SpinnerColumn(),
        *Progress.get_default_columns(),
        TimeElapsedColumn(),
        console=console,
        transient=False,
    ) as progress:
        task1 = progress.add_task("[red]Downloading", total=1000)
        task2 = progress.add_task("[green]Processing", total=1000)
        task3 = progress.add_task("[yellow]Thinking", total=None)

        while not progress.finished:
            progress.update(task1, advance=0.5)
            progress.update(task2, advance=0.3)
            time.sleep(0.01)
            if random.randint(0, 100) < 1:
                progress.log(next(examples))