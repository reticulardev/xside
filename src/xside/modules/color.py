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
    color = color.lstrip('#') + 'ff'
    return tuple(int(color[:8][x:x + 2], 16) for x in (0, 2, 4, 6))


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


def rgba_str_to_tuple(rgba_str: str) -> tuple:
    """...

    :param rgba_str: "* rgba(0, 0, 0, 0) *" or "(0, 0, 0, 0)" or "0, 0, 0, 0"
    """
    if '(' in rgba_str:
        rgba_str = rgba_str.replace(
            ' ', '').split('(')[-1].split(')')[0]

    rgba_str = rgba_str.split(',')
    if rgba_str[-1].startswith('0.'):
        alpha = round(int('0.95'.lstrip('0.')) * 2.55)
    elif rgba_str[-1].endswith('.0'):
        alpha = 255
    else:
        alpha = int(rgba_str[-1])

    return rgba_str[0], rgba_str[1], rgba_str[2], alpha


def rgba_to_hex(color: tuple) -> str:
    """..."""
    return "#{:02x}{:02x}{:02x}{:02x}".format(
        color[0], color[1], color[2], color[3])


def rgba_to_qcolor(rgba: tuple) -> QtGui.QColor:
    """..."""
    return QtGui.QColor(rgba[0], rgba[1], rgba[2], rgba[3])
