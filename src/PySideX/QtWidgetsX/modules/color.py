#!/usr/bin/env python3
import math


def darken_rgba(color: tuple) -> tuple:
    """..."""
    return tuple(
        [0 if x - 20 < 0 else x - 20 for x in color[:-1]] + [color[-1]])


def hex_to_rgba(color: str) -> tuple:
    """..."""
    return tuple(int(color.lstrip('#')[x:x + 2], 16) for x in (0, 2, 4, 6))


def is_dark(color: tuple) -> bool:
    """..."""
    r, g, b, _ = color
    hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
    return False if hsp > 127.5 else True


def lighten_rgba(color: tuple) -> tuple:
    """..."""
    return tuple(
        [255 if x + 20 > 255 else x + 20 for x in color[:-1]] + [color[-1]])


def lighten_hex(color: str) -> str:
    """..."""
    return rgb_to_hex(lighten_rgb(hex_to_rgb(color)))


def rgba_to_hex(color: tuple) -> str:
    """..."""
    return "#{:02x}{:02x}{:02x}{:02x}".format(
        color[0], color[1], color[2], color[3])
