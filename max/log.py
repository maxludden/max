"""This module contains the logging configuration for the project."""
from os import environ
from pathlib import Path
from loguru import logger as log
from max.console import MaxConsole
CWD = Path.cwd()
LOGS = CWD / "logs"
LOG = LOGS / "log.log"
FORMAT = environ.get("LOGURU_FORMAT")
RICH_SUCCESS_LOG_FORMAT = environ.get("RICH_SUCCESS_LOG_FORMAT")
RICH_ERROR_LOG_FORMAT = environ.get("RICH_ERROR_LOG_FORMAT")
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
log.success("Initialized logging")
