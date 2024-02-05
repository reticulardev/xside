#!/usr/bin/env python3
import math


class ColorOp(object):
    """..."""
    def __init__(self, color: str | tuple):
        """..."""
        self.__color = color
        self.__rgb_color = None
        self.__hexa_color = None
        self.__is_dark = False

        self.__update()

    def hex(self) -> str:
        """..."""
        if not self.__hexa_color:
            self.__hexa_color = "#{:02x}{:02x}{:02x}".format(
                self.__rgb_color[0], self.__rgb_color[1], self.__rgb_color[2])
        return self.__hexa_color

    def is_dark(self) -> bool:
        r, g, b = self.rgb()
        hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
        return False if hsp > 127.5 else True

    def rgb(self) -> tuple:
        """..."""
        if not self.__rgb_color:
            self.__rgb_color = tuple(
                int(self.__hexa_color.lstrip('#')[x:x + 2], 16)
                for x in (0, 2, 4))
        return self.__rgb_color

    def __update(self) -> None:
        # ...
        if isinstance(self.__color, str):
            self.__hexa_color = self.__color
        else:
            self.__rgb_color = self.__color
