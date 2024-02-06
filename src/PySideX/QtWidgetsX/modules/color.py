#!/usr/bin/env python3
import math


def rgb_to_hex(color: tuple) -> str:
    """..."""
    return "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])


def is_dark(color: tuple) -> bool:
    r, g, b = color
    hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
    return False if hsp > 127.5 else True


def hex_to_rgb(color: str) -> tuple:
    """..."""
    return tuple(int(color.lstrip('#')[x:x + 2], 16) for x in (0, 2, 4))
