#!/usr/bin/env python3
import logging

from PySide6 import QtGui
from __feature__ import snake_case

import xside.modules.desktopstyles.stylebase as stylebase
import xside.modules.cli as cli
import xside.modules.color as color


class EnvStyleGnome(stylebase.EnvStyle):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)

    def contex_menu(self) -> dict:
        """..."""
        rgb = ' '.join(self.main_window()['background-color'].split()[:-1])
        return {
            'background-color': rgb + ' 255)',
            'border': self.main_window()['border'],
            'border-radius': f'{self.main_window()["border-radius"]}',
            'margin': '0px 0px 0px 0px',
            'padding': '6px 6px 6px 6px',
            'spacing': '0px',
        }

    def contex_menu_separator(self) -> dict:
        """..."""
        bg_color = self.palette.color(QtGui.QPalette.Window).to_tuple()
        step_tone = 15 if color.is_dark(bg_color) else 30
        r, g, b, a = color.lighten_rgba(bg_color, step_tone)

        return {
            'color': f'rgba({r}, {g}, {b}, {a})',
            'margin': '8px 6px 8px 6px',
        }

    def contex_menu_button(self) -> dict:
        """..."""
        r = self.contex_menu()['border-radius'].split('px')[0]
        r = int(r) - 4 if int(r) > 6 else r
        return {
            'border-radius': f'{r}px',
            'padding': '6px 12px 6px 12px',
        }

    def contex_menu_button_hover(self) -> dict:
        """..."""
        r, g, b, _ = self.palette.color(
            QtGui.QPalette.AlternateBase).to_tuple()
        return {
            'background-color': f'rgba({r}, {g}, {b}, 255)',
            'border': f'1px solid rgba({r}, {g}, {b}, 255)'
        }

    @staticmethod
    def context_menu_group() -> dict:
        """..."""
        return {
            'padding': '6px 12px 6px 14px',
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
            'border-radius': '10px',
            'margin': '0px 0px 0px 0px',
        }

    @staticmethod
    def window_icon() -> dict:
        """..."""
        return {
            'margin': '5px 7px 5px 7px',
        }
