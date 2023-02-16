"""This module defines a custom progress bar for the max console."""

import time
from random import randint
from typing import Sequence, Tuple


from rich.panel import Panel
# from rich import inspect
from rich.progress import (
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

from max.console import MaxConsole, Console

progress_console = MaxConsole()


class MaxProgress(Progress):
    """Generates a progress bar for MaxConsole with additional fields\
        and color_pallets."""

    columns: Sequence[ProgressColumn]
    console: MaxConsole

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not self.console:
            self.console =  MaxConsole()
        if not self.columns:
            self.columns = self.get_default_columns()
        if self.expand is None:
            self.expand = True

    @classmethod
    def get_default_columns(cls) -> Tuple[ProgressColumn, ...]:
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
                if progress.tasks[0].completed is 1000:
                    progress.update(task2, advance=2)

            time.sleep(0.01)
            if randint(0, 100) < 1:
                progress.log(next(examples))
                    