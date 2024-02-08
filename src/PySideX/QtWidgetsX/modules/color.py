#!/usr/bin/env python3
import math

from PySide6 import QtGui
from __feature__ import snake_case


def darken_rgba(color: tuple, step: int = 10) -> tuple:
    """..."""
    return tuple(
        [0 if x - step < 0 else x - step for x in color[:-1]] + [color[-1]])


def darken_hex(color: str, step: int = 10) -> str:
    """..."""
    rgba_dark = darken_rgba(hex_to_rgba(color), step)
    return "#{:02x}{:02x}{:02x}{:02x}".format(
        rgba_dark[0], rgba_dark[1], rgba_dark[2], rgba_dark[3])


def hex_to_rgba(color: str) -> tuple:
    """..."""
    return tuple(int(color.lstrip('#')[x:x + 2], 16) for x in (0, 2, 4, 6))


def is_dark(color: tuple) -> bool:
    """..."""
    r, g, b, _ = color
    hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
    return False if hsp > 127.5 else True


def lighten_rgba(color: tuple, step: int = 10) -> tuple:
    """..."""
    return tuple(
        [255 if x + step > 255 else x + step for x in color[:-1]] +
        [color[-1]])


def lighten_hex(color: str, step: int = 10) -> str:
    """..."""
    rgba_light = lighten_rgba(hex_to_rgba(color), step)
    return "#{:02x}{:02x}{:02x}{:02x}".format(
        rgba_light[0], rgba_light[1], rgba_light[2], rgba_light[3])


def qcolor_to_rgba(qcolor: QtGui.QColor, alpha_float: bool = False) -> tuple:
    alpha = qcolor.alpha_f() if alpha_float else qcolor.alpha()
    return qcolor.red(), qcolor.green(), qcolor.blue(), alpha


def rgba_to_hex(color: tuple) -> str:
    """..."""
    return "#{:02x}{:02x}{:02x}{:02x}".format(
        color[0], color[1], color[2], color[3])
