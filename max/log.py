"""This module contains the logging configuration for the project."""
# pylint: disable=W0622:redefined-builtin
from functools import wraps
from pathlib import Path

from loguru import logger as log

from max.console import MaxConsole

CWD = Path.cwd()
LOGS = CWD / "logs"
LOG = LOGS / "log.log"
FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS}|{level: <8}|{name}|{function}|\
Line {line:^5}|{message}"
RICH_SUCCESS_LOG_FORMAT = "[bold #0088ff]{time:YYYY-MM-DD HH:mm:ss.SSS}[/]|\
[bold #00ffff]{level:^10}[/]|[bold #ffff00]{file.name:^10}[/]|\
[bold #ff8800] Line {line:^5}[/]|[bold #00ff00] {message}[/]"
RICH_ERROR_LOG_FORMAT = "[bold #0088ff]{time:YYYY-MM-DD HH:mm:ss.SSS}[/]|\
[bold #00ffff]{level:^10}[/]|[bold #ffff00]{file.name:^10}[/]|\
[bold #ff8800] Line {line:^5}[/]|[bold #ff8800] {message}[/]"
SNOOP_LOGGING = "True"

console = MaxConsole()

log.remove()
log.add(sink=LOG, level="DEBUG", format=FORMAT, diagnose=True, backtrace=True)
log.add(
    sink=lambda msg: console.log(
        msg, justify="left", style="logging.level.info", highlight=True
    ),
    level="INFO",
    format=RICH_SUCCESS_LOG_FORMAT,
    diagnose=True,
    backtrace=True,
)
log.add(
    sink=lambda msg: console.log(
        msg, justify="left", style="logging.level.error", highlight=True
    ),
    level="ERROR",
    format=RICH_ERROR_LOG_FORMAT,
    diagnose=True,
    backtrace=True,
    catch=True,
)
console.clear()
console.line(2)
log.debug("Initialized logging")


def debug(*, entry=True, exit=True, level="DEBUG"):
    """Log the entry and exit of a function."""

    def wrapper(func):
        name = func.__name__

        @wraps(func)
        def wrapped(*args, **kwargs):
            _logger = log.opt(depth=1)
            if entry:
                _logger.log(
                    level, "Entering '{}' (args={}, kwargs={})", name, args, kwargs
                )
            result = func(*args, **kwargs)
            if exit:
                _logger.log(level, "Exiting '{}' (result={})", name, result)
            return result

        return wrapped

    return wrapper
