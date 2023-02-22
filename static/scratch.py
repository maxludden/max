
        split_text = Gradient.split_text(input_text, num)

        for x, string in enumerate(self.gradient_strings, start=1):
            console.log(f"[bold #ff00ff]Index {x}.[bold #00ff00] {string}[/]")

        # if index < num - 1:
        #     color1 = self.colors[index]
        #     console.log(f"Color{index}: [{color1.as_style()}]{color1}[/]")
        #     r1, g1, b1 = color1.as_rgb()
        #     color2 = self.colors[next_index]
        #     console.log(f"Color{index+1}: [{color2.as_style()}]{color2}[/]")
        #     r2, g2, b2 = color2.as_rgb()

        #     dr = r2 - r1
        #     dg = g2 - g1
        #     db = b2 - b1
        # elif index == num:
        #     color1 = self.colors[index]
        #     console.log(f"Color{index}: [{color1.as_style()}]{color1}[/]")
        #     r1, g1, b1 = color1.as_rgb()
        #     color2 = self.colors[next_index]
        #     console.log(f"Color{index+1}: [{color1.as_style()}]{color2}[/]")

        # for index in range(gradient_size):
        #     blend = index / gradient_size
        #     color = f"#{int(r1 + dr * blend):02X}"
        #     color = f"{color}{int(g1 + dg * blend):02X}"
        #     color = f"{color}{int(b1 + db * blend):02X}"
        #     _substring.stylize(color, index, index + 1)
        # console.log(f"IndexSubstring: {_substring}")
        # text = Text.assemble(text, _substring, justify="left")

        # gradient_text = Text.assemble(gradient_text,text, justify="left")
        # return text