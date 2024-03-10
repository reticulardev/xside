#!/usr/bin/env python3
import os
import pathlib
import sys

from PySide6 import QtGui
from __feature__ import snake_case

import xside.modules.color as color
import xside.modules.desktopstyles.stylebase as stylebase


class EnvStyleWindows11(stylebase.EnvStyle):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)

    @staticmethod
    def control_buttons() -> dict:
        """..."""
        return {
            'margin': '0px 0px 0px 0px',
            'spacing': '0px',
            'border': '0px',
        }

    @staticmethod
    def header_bar() -> dict:
        """..."""
        return {
            'margin': '0px 0px 0px 0px',
        }

    def main_window(self) -> dict:
        """..."""
        bg_color = self.palette.color(QtGui.QPalette.Window).to_tuple()
        bg_r, bg_g, bg_b, bg_a = bg_color

        bd_r, bd_g, bd_b, bd_a = color.lighten_rgba(
            bg_color, 15) if color.is_dark(bg_color) else color.darken_rgba(
            bg_color, 50)

        return {
            'background-color': f'rgba({bg_r}, {bg_g}, {bg_b}, {bg_a})',
            'border': f'1px solid rgba({bd_r}, {bd_g}, {bd_b}, {bd_a})',
            'margin': '0px 0px 0px 0px',
            'border-radius': '8px',
            'border-top-left-radius': '8px',
            'border-top-right-radius': '8px',
            'border-bottom-right-radius': '0px',
            'border-bottom-left-radius': '0px',
        }

    @staticmethod
    def window_icon() -> dict:
        """..."""
        return {
            'margin': '5px 5px 5px 5px',
        }
