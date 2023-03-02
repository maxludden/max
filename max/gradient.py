"""This module contains the gradient class to automate the creation of gradient colored text."""
# pylint: disable=W0611:unused-import
# pylint: disable=C0103:invalid-name
# pylint: disable=W0612:unused-variable
# pylint: disable=R0913:too-many-arguments
import re
from os import environ
from typing import Optional, Tuple

from cheap_repr import normal_repr, register_repr
from lorem_text import lorem
from rich.console import JustifyMethod, RenderResult
from rich.control import strip_control_codes
from rich.text import Text
from snoop import snoop

from max.color_index import ColorIndex
from max.console import MaxConsole
from max.log import debug, log
from max.named_color import (
    ColorParsingError,
    InvalidHexColor,
    InvalidRGBColor,
    NamedColor,
)
