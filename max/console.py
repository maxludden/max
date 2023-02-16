"""MaxConsole is a custom themed class inheriting from rich.console.Console."""

import threading
from dataclasses import dataclass

from rich.console import Console, ConsoleRenderable, RichCast
from rich.theme import Theme
from rich.traceback import install as install_traceback

from max.theme import MaxTheme

RenderableType = ConsoleRenderable | RichCast | str


class Singleton(type):
    """Singleton metaclass for MaxConsole."""

    _instance_lock = threading.Lock()

    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            with Singleton._instance_lock:
                cls.__instance = super().__call__(*args, **kwargs)
                return cls.__instance
        else:
            return cls.__instance


@dataclass
class MaxConsole(Console, metaclass=Singleton):
    """A custom themed console class that inherits from rich.console.Console"""
    theme: Theme = MaxTheme()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, theme=self.theme)
        install_traceback(console=self)

    def __call__(self, *args, **kwargs):
        return self

    def __enter__(self):
        return self

    def get_max_console(self):
        """Generates a global instance of MaxConsole if one is not provided."""
        return self
    