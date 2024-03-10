#!/usr/bin/env python3
import os
import pathlib
import sys

from PySide6 import QtGui
from __feature__ import snake_case

from xside.modules.parser import DesktopFile
import xside.modules.desktopstyles.stylebase as stylebase
import xside.modules.color as color


class EnvStylePlasma(stylebase.EnvStyle):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)

    def contex_menu(self) -> dict:
        """..."""
        return {
            'background-color': self.main_window()['background-color'],
            'border': self.main_window()['border'],
            'border-radius': '3px',
            'margin': '0px 0px 0px 0px',
            'padding': '3px 3px 3px 3px',
            'spacing': '0px',
        }

    def contex_menu_separator(self) -> dict:
        """..."""
        bg_color = self.palette.color(QtGui.QPalette.Window).to_tuple()
        step_tone = 15 if color.is_dark(bg_color) else 30
        r, g, b, a = color.lighten_rgba(bg_color, step_tone)

        return {
            'color': f'rgba({r}, {g}, {b}, {a})',
            'margin': '3px 3px 3px 3px',
        }

    def contex_menu_button(self) -> dict:
        """..."""
        r = self.contex_menu()['border-radius'][0]
        r = int(r) - 4 if int(r) > 6 else r
        return {
            'border-radius': f'{r}px',
            'padding': '2px 6px 2px 6px',
        }

    def contex_menu_button_hover(self) -> dict:
        """..."""
        r, g, b, a = self.accent_color.to_tuple()
        return {
            'background-color': f'rgba({r}, {g}, {b}, 100)',
            'border': f'1px solid rgba({r}, {g}, {b}, {a})',
        }

    @staticmethod
    def context_menu_group() -> dict:
        """..."""
        return {
            'padding': '2px 6px 2px 8px',
        }

    @staticmethod
    def control_buttons() -> dict:
        """..."""
        return {
            'margin': '0px 0px 0px 0px',
            'spacing': '6px',
        }

    @staticmethod
    def header_bar() -> dict:
        """..."""
        return {
            'margin': '3px 5px 0px 5px',
        }

    def main_window(self) -> dict:
        """..."""
        bg_color = self.palette.color(QtGui.QPalette.Window).to_tuple()
        bg_r, bg_g, bg_b, bg_a = bg_color

        step_tone = 15 if color.is_dark(bg_color) else 30
        bd_r, bd_g, bd_b, bd_a = color.lighten_rgba(bg_color, step_tone)

        return {
            'background-color': f'rgba({bg_r}, {bg_g}, {bg_b}, {bg_a})',
            'border': f'1px solid rgba({bd_r}, {bd_g}, {bd_b}, {bd_a})',
            'margin': '0px 0px 0px 0px',
            'border-top-left-radius': '4px',
            'border-top-right-radius': '4px',
            'border-bottom-right-radius': '0px',
            'border-bottom-left-radius': '0px',
        }

    @staticmethod
    def window_icon() -> dict:
        """..."""
        return {
            'margin': '0px 0px 0px 0px',
        }
