"""This module defines a custom progress bar for the max console."""
import threading
import time
from random import randint
from typing import Sequence, Tuple, Optional, Dict


from rich.panel import Panel
# from rich import inspect
from rich.progress import (
    TaskID,
    BarColumn,
    MofNCompleteColumn,
    Progress,
    ProgressColumn,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.rule import Rule
from rich.style import Style
from rich.syntax import Syntax
from rich.table import Column, Table
from rich.text import Text

from max.console import MaxConsole,RenderableType

console = MaxConsole()

class MaxProgressColumn(ProgressColumn):
    """A basic wrapper around `rich.table.Column`"""
    def __init__(self, table_column: Optional[Column] = None) -> None:
        super().__init__(table_column=table_column)
        self._table_column = table_column
        self._renderable_cache: Dict[TaskID, Tuple[float, RenderableType]] = {}
        self._update_time: Optional[float] = None

    def get_table_column(self) -> Column:
        """Get a table column, used to build tasks table."""
        return self._table_column or Column()


def singleton(cls):
    """Singleton decorator for MaxProgress."""
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

class MaxProgress(Progress):
    """Generates a progress bar for MaxConsole with additional fields\
        and color_pallets.
    Args:
    console (Console, optional): Optional Console instance. Default will \
        an internal Console instance writing to stdout.
    auto_refresh (bool, optional): Enable auto refresh. If disabled, \
        you will need to call refresh().
    refresh_per_second (Optional[float], optional): Number of times per \
        second to refresh the progress information or None to use \
        default (10). Defaults to None. 
    speed_estimate_period (float, optional): Period (in seconds) used to calculate \
        the speed estimate. Defaults to 30. 
    transient: (bool, optional): Clear the progress on exit. Defaults to False. 
    redirect_stdout: (bool, optional): Enable redirection of stdout, so print \
        may be used. Defaults to True. 
    redirect_stderr: (bool, optional): Enable redirection of stderr. Defaults to True. 
    get_time: (Callable, optional): A callable that gets the current time, or \
        None to use Console.get_time. Defaults to None.
    disable (bool, optional): Disable progress display. Defaults to False
    expand (bool, optional): Expand tasks table to fit width. Defaults to False.    
    """

    columns: Sequence[MaxProgressColumn]
    progress_console: MaxConsole = MaxConsole()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not self.progress_console:
            self.progress_console =  MaxConsole()
        if not self.columns:
            self.columns = self.get_default_columns()
        if self.expand is None:
            self.expand = True

    @classmethod
    def get_default_columns(cls) -> Tuple[MaxProgressColumn, ...]:
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
                SpinnerColumn(), # Redundant spinner left of default columns
                *MaxProgress.get_max_columns(),
                "Elapsed:",
                TimeElapsedColumn(), # Redundant elapsed time right of default columns
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
    console.clear()
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

    console = MaxConsole(record=True)

    with MaxProgress() as progress:
        task1 = progress.add_task("[red]Downloading", total=1000)
        task2 = progress.add_task("[green]Processing", total=1000)
        task3 = progress.add_task("[yellow]Thinking", total=None)

        while not progress.finished:
            progress.update(task1, advance=1)
            progress.update(task2, advance=0.7)
            if progress.tasks[0].completed >= 400:
                if progress.tasks[0].completed < 500:
                    progress.start_task(task3)
                    progress.update(task3, total=1000)
                    progress.update(task3, completed=200)
                    progress.update(task3, description="[bold #00ff00]Planning![/]")
                progress.update(task3, advance=2)
                if progress.tasks[0].completed > 999:
                    progress.update(task1, description="[dim #00ff00]Downloaded[/]")
                    progress.update(task2, advance=2)
                if progress.tasks[2].completed > 999:
                    progress.update(task3, description="[dim #00ff00]Planned![/]")
                if progress.tasks[1].completed > 999:
                    progress.update(task2, description="[dim #00ff00]Processed![/]")

            time.sleep(0.01)
            if randint(0, 100) < 1:
                progress.log(next(examples))
    console.line(3)
                    