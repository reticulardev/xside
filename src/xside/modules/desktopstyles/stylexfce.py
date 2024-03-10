#!/usr/bin/env python3
import logging

from PySide6 import QtGui
from __feature__ import snake_case

import xside.modules.color as color
import xside.modules.desktopstyles.stylebase as stylebase


class EnvStyleXFCE(stylebase.EnvStyle):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)

    def contex_menu(self) -> dict:
        """..."""
        rgb = ' '.join(self.main_window()['background-color'].split()[:-1])

        bg_color = self.palette.color(QtGui.QPalette.Window).to_tuple()
        bd_r, bd_g, bd_b, bd_a = (50, 50, 50, 255) if color.is_dark(
            bg_color) else (180, 180, 180, 255)
        return {
            'background-color': rgb + ' 255)',
            'border': f'1px solid rgba({bd_r}, {bd_g}, {bd_b}, {bd_a})',
            'border-radius': '0px',
            'margin': '0px 0px 0px 0px',
            'padding': '1px 6px 1px 6px',
            'spacing': '0px',
        }

    def contex_menu_button(self) -> dict:
        """..."""
        r = self.contex_menu()['border-radius'].split('px')[0]
        r = int(r) - 4 if int(r) > 6 else r
        return {
            'border-radius': f'{r}px',
            'padding': '2px 4px 2px 4px',
        }

    def contex_menu_button_hover(self) -> dict:
        """..."""
        r, g, b, _ = self.accent_color.to_tuple()
        bd_r, bd_g, bd_b, bd_a = color.darken_rgba(
            self.accent_color.to_tuple(), 50)
        return {
            'background-color': f'rgba({r}, {g}, {b}, 255)',
            'border': f'1px solid rgba({bd_r}, {bd_g}, {bd_b}, {bd_a})',
        }

    @staticmethod
    def context_menu_group() -> dict:
        """..."""
        return {
            'padding': '2px 4px 2px 6px',
        }

    def contex_menu_separator(self) -> dict:
        """..."""
        bg_color = self.palette.color(QtGui.QPalette.Window).to_tuple()
        r, g, b, a = (50, 50, 50, 255) if color.is_dark(
            bg_color) else (180, 180, 180, 255)
        return {
            'color': f'rgba({r}, {g}, {b}, {a})',
            'margin': '1px 0px 1px 0px',
        }

    def main_window(self) -> dict:
        """..."""
        bg_color = self.palette.color(QtGui.QPalette.Window).to_tuple()
        dark = color.is_dark(bg_color)
        bg_r, bg_g, bg_b, bg_a = bg_color
        bd_r, bd_g, bd_b, bd_a = color.lighten_rgba(
            bg_color, 30) if dark else color.darken_rgba(bg_color, 60)

        return {
            'background-color': f'rgba({bg_r}, {bg_g}, {bg_b}, {bg_a})',
            'border': f'1px solid rgba({bd_r}, {bd_g}, {bd_b}, {bd_a})',
            'margin': '0px 0px 0px 0px',
            'border-top-left-radius': '8px',
            'border-top-right-radius': '8px',
            'border-bottom-right-radius': '0px',
            'border-bottom-left-radius': '0px',
        }
