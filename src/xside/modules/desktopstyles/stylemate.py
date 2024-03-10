#!/usr/bin/env python3
import logging

from PySide6 import QtGui
from __feature__ import snake_case

import xside.modules.desktopstyles.stylexfce as stylexfce
import xside.modules.color as color


class EnvStyleMate(stylexfce.EnvStyleXFCE):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)

    def contex_menu(self) -> dict:
        """..."""
        bg_color = self.palette.color(QtGui.QPalette.Window).to_tuple()
        bd_r, bd_g, bd_b, bd_a = (80, 80, 80, 255) if color.is_dark(
            bg_color) else (180, 180, 180, 255)
        return {
            'background-color': self.main_window()['background-color'],
            'border': f'1px solid rgba({bd_r}, {bd_g}, {bd_b}, {bd_a})',
            'border-radius': f'{self.main_window()["border-radius"]}',
            'margin': '0px 0px 0px 0px',
            'padding': '4px 4px 4px 4px',
            'spacing': '0px',
        }

    @staticmethod
    def contex_menu_button() -> dict:
        """..."""
        return {
            'border-radius': '0px',
            'padding': '4px 6px 4px 6px',
        }

    def contex_menu_button_hover(self) -> dict:
        """..."""
        bg_color = self.palette.color(QtGui.QPalette.Window).to_tuple()
        r, g, b, a = (62, 62, 62, 255) if color.is_dark(bg_color) else (
            222, 222, 222, 255)
        return {
            'background-color': f'rgba({r}, {g}, {b}, {a})',
            'border': f'1px solid rgba({r}, {g}, {b}, {a})',
        }

    def context_menu_button_label_hover(self) -> dict:
        """..."""
        r, g, b, a = self.palette.color(
            QtGui.QPalette.Active, QtGui.QPalette.WindowText).to_tuple()
        return {
            'color': f'rgba({r}, {g}, {b}, {a})',
        }

    def contex_menu_separator(self) -> dict:
        """..."""
        bg_color = self.palette.color(QtGui.QPalette.Window).to_tuple()
        r, g, b, a = (80, 80, 80, 255) if color.is_dark(bg_color) else (
            200, 200, 200, 255)
        return {
            'color': f'rgba({r}, {g}, {b}, {a})',
            'margin': '0px 4px 0px 4px',
        }
