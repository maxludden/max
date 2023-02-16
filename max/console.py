import threading
from typing import IO, Dict, List, Mapping, Optional, Sequence

from rich.console import Console, ConsoleOptions, NewLine, RenderResult
from rich.style import Style, StyleType
from rich.theme import Theme
from rich.traceback import install as install_traceback

from max.theme import MaxTheme


class Singleton(type):
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


class MaxConsole(Console, metaclass=Singleton):
    """A custom themed console class that inherits from rich.console.Console"""

    theme: Theme

    def __init__(self, theme: Theme = MaxTheme(), *args, **kwargs):
        super().__init__(*args, **kwargs, theme=theme)
        install_traceback(console=self)

    def __call__(self, *args, **kwargs):
        return self

    def __enter__(self):
        return self

    def get_max_console(self):
        return self