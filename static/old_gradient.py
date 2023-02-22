class Gradient(Text):
    """A class for generating gradient text in the terminal."""

    """
    _text: str
    style: str | Style | StyleStack
    justify: Optional[JustifyMethod]
    overflow: Optional[OverflowMethod]
    no_wrap: Optional[bool]
    end: str
    tab_size: Optional[int]
    _spans: list[Span | None]
    _length: int
    
    The above attributes are inherited from the Text class.
    """
    start_color: Optional[NamedColor]
    end_color: Optional[NamedColor]
    _start: Optional[int]
    _end: Optional[int]
    _invert: Optional[bool]
    _num_of_index: Optional[int]
    _color_index: ColorIndex
    _color_range: list[NamedColor]
    title: Optional[str]

    __slots__ = [
        "_text",
        "style",
        "justify",
        "overflow",
        "no_wrap",
        "end",
        "tab_size",
        "_spans",
        "_length",
        "starting_color",
        "ending_color",
        "_start",
        "_end",
        "invert",
        "_num_of_index",
        "color_index",
        "color_range",
    ]

    def __init__(
        self,
        text: str = "",
        starting_color: Optional[NamedColor | str] = None,
        ending_color: Optional[NamedColor | str] = None,
        justify: Optional[JustifyMethod] = None,
        overflow: Optional[OverflowMethod] = None,
        no_wrap: Optional[bool] = None,
        end: str = "\n",
        tab_size: Optional[int] = 8,
        spans: Optional[list[Span]] = None,
        invert: Optional[bool] = None,
        num_of_colors: int = 3,
        title: Optional[str] = f"Gradient",
    ) -> None:
        """
        Initialize a new instance of gradient text. The only required argument is the message\
        to be displayed. Used as such, the gradient will be randomly generated and applied to\
        the message.

        If a start and end color are provided the gradient will be generated between those two colors.

        Args:
        - text (`Optional[str]`): Default unstyled text. Defaults to "".

        - starting_color (`Optional[NamedColor]`): The starting color of the gradient. Defaults to None.\
                Valid colors are any color, hex value, or rgb color that could be parsed into NamedColor.

        - ending_color (`Optional[NamedColor]`): The ending color of the gradient. Defaults to None.\
                Valid colors are any color, hex value, or rgb color that could be parsed into NamedColor.

        - justify (`Optional[JustifyMethod]`): Literal['left', 'center', 'full', 'right']. Defaults to None.

        - overflow (`Optional[OverflowMethod]`): Literal['crop', 'fold', 'ellipsis']. Defaults to None.

        - no_wrap (`Optional[bool]`): Disable text wrapping, or None for default. Defaults to None.

        - end (`Optional[str]`): Character to end text with. Defaults to "\\\\n".

        - tab_size (`Optional[int])`: Number of spaces per tab, or ``None`` to use ``console.tab_size``. Defaults to 8.

        - spans (`Optional[list[Span]]`). A list of predefined style spans. Defaults to None.

        - invert (`Optional[bool]`): Whether the gradient will ascend or descend the color spectrum. Defaults\
              to None which will pick a direction at random.

        - num_of_colors (`Optional[int`]): The number of colors to include in a randomly generated gradient.\
                Defaults to 3. This value is overruled if both `start_input` and `end_input` are provided.

        - title (`Optional[str]`): The title of the Gradient Instance. Defaults to "Gradient".
        """
        # Initialize the Text class
        super().__init__(
            text,
            style=None,
            justify=justify,
            overflow=overflow,
            no_wrap=no_wrap,
            end=end,
            tab_size=tab_size,
            spans=spans,
        )
        sanitized_text = strip_control_codes(text)
        self._text = [sanitized_text]
        self.starting_color = starting_color
        self.ending_color = ending_color
        self.justify = justify
        self.overflow = overflow
        self.no_wrap = no_wrap
        self.end = end
        self.tab_size = tab_size
        self._spans = spans or []
        self._length = len(sanitized_text)
        self.title = self._gradient_title()
        self._color_range = []
        self.num_of_index = num_of_colors + 1

        # Determine if the gradient is inverted
        match invert:
            case True:
                self._invert = True
            case False:
                self._invert = False
            case None:
                self._invert = choice([True, False])

        # Validate inputs and generate the color index
        valid_start = self.validate_color(starting_color)
        valid_end = self.validate_color(ending_color)

        # Validate/generate the start and end colors
        match (valid_start, valid_end):
            case (True, True):  # If both inputs are valid
                self.start_color, self.end_color = valid_start, valid_end

            case (True, False):  # If only start input is valid
                self._start = NamedColor(starting_color).as_index()
                self._end = self._generate_end_from_start()

            case (False, True):  # If only end input is valid
                self._end = NamedColor(ending_color).as_index()
                self._start = self._generate_start_from_end()

            case (False, False):  # If neither colors are valid
                self._start, self._end = self._generate_start_end()

        # Generate the color index
        start_index = self.start_color.as_index()
        end_index = self.end_color.as_index()

        self._color_index = ColorIndex(self._start, self._end, self._invert).indexes

        # # Generate color_range from color_index
        # for i in self._color_index:
        #     color = NamedColor.colors[i]
        #     named_color = NamedColor(color)
        #     self._color_range.append(named_color)

        # self.num_of_index = len(self._color_range)
        # self._length = len(self._text)
        # gradient_size = self._length // self.num_of_index - 1

        # for index in range(self.num_of_index - 1):
        #     next_index = index + 1
        #     begin = index * gradient_size
        #     end = begin + gradient_size
        #     substring = self.text[begin:end]

        #     if index < self.num_of_index - 1:
        #         color1 = NamedColor(self._color_range[index])
        #         r1, g1, b1 = color1.as_rgb()
        #         color2 = NamedColor(self._color_range[next_index])
        #         r2, g2, b2 = color2.as_rgb()
        #         dr = r2 - r1
        #         dg = g2 - g1
        #         db = b2 - b1

        #     # Generate Blend
        #     for index in range(gradient_size):
        #         blend = index / gradient_size
        #         color = f"#{int(r1 + dr * blend):02X}{int(g1 + dg * blend):02X}{int(b1 + db * blend):02X}"  # type: ignore
        #         substring.stylize(color, index, index + 1)

        #     # Generate gradient text for substring
        #     self.text = Text.assemble(self.text, substring, justify=justify)

    def __len__(self) -> int:
        return super().__len__()

    def __bool__(self) -> bool:
        return super().__bool__()

    def __bool__(self) -> bool:
        return super().__bool__()

    def __str__(self) -> str:
        return super().__str__()

    @staticmethod
    def validate_color(
        color: None | str | int | NamedColor, verbose: bool = False
    ) -> bool:
        """Validate the starting color.

        Args:
            color (`None|str|int|NamedColor`): The starting color of the gradient.
            verbose (`Optional[bool]`): Whether to print the validation result. Defaults to False.

        Returns:
            `bool`: True if the starting color is valid, False otherwise.
        """
        if isinstance(color, (None, str, int, NamedColor)):
            valid = True
        else:
            valid = False
        if verbose:
            if valid:
                console.log(
                    f"[bold underline #00ff00]Color {color} is valid:thumbs_up_light_skin_tone:[/]"
                )
            else:
                console.log(
                    f"[bold underline #ff0000]Color {color} is invalid:thumbs_down_light_skin_tone:[/]"
                )

    def _generate_start_from_end(self) -> int:
        """Generates the color starting the gradient from the ending color."""
        if self.invert:
            step = 1
        else:
            step = -1

        __start = NamedColor(self.ending_color).as_index + (step * self.num_of_index)
        if __start < 0:
            _start = __start + 10
        else:
            _start = __start
        if _start > 9:
            start = _start - 10
        else:
            start = _start

        self._start = int(start)
        return self._start

    def _generate_end_from_start(self) -> int:
        """Generates the color ending the gradient from the starting color."""
        if self.invert:
            step = -1
        else:
            step = 1
        __end = NamedColor(self.starting_color).as_index + (step * self.num_of_index)
        if __end < 0:
            _end = __end + 10
        else:
            _end = __end
        if end > 9:
            end = _end - 10
        else:
            end = _end
        self._end = int(end)
        return self._end

    def _generate_start_end(self) -> tuple[int, int]:
        """Generate a random starting and ending color."""
        self._start = randint(0, 9)  # start
        if self.num_of_index is None:
            raise ColorParsingError(
                "Unable to generate a gradient without a starting\
                    color, ending color, or number of colors."
            )

        # invert
        if self._invert:
            step = -1
        else:
            step = 1

        __end = self._start + (step * self.num_of_index)  # range

        # ensure that the ColorIndex stays within the range of 0-9
        if __end < 0:
            _end = __end + 10
        else:
            _end = __end
        if _end > 9:
            end = _end - 10
        else:
            end = _end
        self._end = int(end)
        return self._start, self._end

    def _color_range_as_str(
        self, format: Literal["name", "hex", "rgb", "int"] = "name", end: str = ", "
    ) -> str:
        """Generates a string concatenating the gradients color together.

        Args:
            format (`Literal['name', 'hex', 'rgb', 'int']`, optional): The format of the color. Defaults to 'name'.
            end (`str`, optional): The end of the string. Defaults to ', '.
        """
        range = []
        for color in self._color_range:  # loop through color_index
            match format:
                case "name":
                    range.append(color.value)
                case "hex":
                    range.append(color.as_hex())
                case "rgb":
                    range.append(color.as_rgb())
                case "int":
                    range.append(color.as_index())
                case _:
                    raise ValueError(f"Invalid format: {format}")
        return end.join(str(color) for color in range)

    def __repr__(self) -> str:
        colors = self._color_range_as_str()
        return f"<Gradient: {colors} >"

    def _gradient_title(self) -> str:
        """Generate the title of the gradient.

        Args:
            start_input (`Any`, optional): The color from which to start the gradient. Defaults to None.
            end_input (`Any`, optional): The color to end the gradient. Defaults to None.
            num_of_index (`int`, optional): The number of colors in the gradient. Defaults to 3.

        Returns:
            str: The gradient's title.
        """
        if self.title == "Gradient":
            color_str = self._color_range_as_str()
            self.title = f"< Gradient: {color_str} >"
            return self.title
        else:
            return self.title

    def _parse_start(self) -> NamedColor | None:
        """
        Parse starting_colo for the beginning color of the gradient gradient. Valid\
            inputs are NamedColor objects, their names, or their HEX values.

        Args:
            start_input (`Optional[NamedColor|str]`): The color from which to start the gradient.

        Returns:
            `Tuple[NamedColor, NamedColor]``None`: If both inputs can be instantiated\
                  as NamedColors, return a tuple of the two colors. Otherwise, return None.
        """
        # Named Color
        if isinstance(self.starting_color, NamedColor):  # NamedColor object
            self._start = self.starting_color
            return self._start
        elif isinstance(self.starting_color, str):
            # NamedColor Value
            if self.starting_color in NamedColor.colors:
                self._start = NamedColor(self.starting_color)
                return self._start
            # NamedColor as Hex
            if self.starting_color.startswith("#"):
                if self.starting_color in NamedColor.hex_values:
                    self._start = NamedColor(self.starting_color)
                    return self._start
                else:
                    raise ColorParsingError(
                        f"Invalid starting color string: {self.starting_color}\n \
                                            Valid Colors: {NamedColor.colors}, \
                                            {NamedColor.hex_values}"
                    )
            else:
                raise ColorParsingError(
                    f"Invalid starting color string: {self.starting_color}\n \
                                            Valid Colors: {NamedColor.colors}, \
                                            {NamedColor.hex_values}, \
                                            {NamedColor.rgb_values}"
                )
        # RGB value
        elif isinstance(self.starting_color, Tuple):
            if self.starting_color in NamedColor.rgb_values:
                self._start = NamedColor(self.starting_color)
                return self._start
            else:
                raise ColorParsingError(
                    f"Invalid starting color tuple: {self.starting_color}\n \
                                        Valid Colors: {NamedColor.colors}, \
                                        {NamedColor.hex_values}, {NamedColor.rgb_values}"
                )

        def __parse_start(self) -> NamedColor:
            try:
                color = NamedColor(self.starting_color)
            except ColorParsingError as cpe:
                raise ColorParsingError(cpe, f"starting_color: {self.starting_color}")

    def __len__(self) -> int:
        return len(self._color_index)
