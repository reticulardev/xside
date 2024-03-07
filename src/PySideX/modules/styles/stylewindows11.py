#!/usr/bin/env python3
import os
import sys

from PySide6 import QtGui
from __feature__ import snake_case

import PySideX.modules.color as color
import PySideX.modules.styles.style as style

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)


class EnvStyleWindows11(style.EnvStyle):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)

    @staticmethod
    def controlbutton_margin() -> tuple:
        """..."""
        return 0, 0, 0, 0

    @staticmethod
    def controlbutton_order() -> tuple:
        """XAI M -> (2, 1, 0), (3,)

        Close     Max       Min       Icon      Above all
        X = 2     A = 1     I = 0     M = 3     F = 4

        (2, 1, 0), (3,) -> [Close Max Min ............. Icon]
        """
        return (3,), (0, 1, 2)

    @staticmethod
    def controlbutton_style(
            window_is_dark: bool,
            button_name: str,
            button_state: str) -> str:
        """..."""
        # window_is_dark: True or False
        # button_name: 'minimize', 'maximize', 'restore' or 'close'
        # button_state: 'normal', 'hover', 'inactive'

        if button_name == 'minimize':
            button_name = 'go-down'
        elif button_name == 'maximize':
            button_name = 'go-up'
        elif button_name == 'restore':
            button_name = 'window-restore'
        else:
            button_name = 'window-close'

        if button_state == 'hover':
            button_name += '-hover'
        if button_state == 'inactive':
            button_name += '-inactive'

        if window_is_dark:
            button_name += '-symbolic'

        url_icon = os.path.join(
            SRC_DIR, 'static',
            'windows-11-control-buttons', button_name + '.svg')

        return (
            'ControlButton {'
            f'background: url({url_icon}) center no-repeat;'
            f'width: 42px;'
            'height: 26px;'
            'border-radius: 0px;'
            'border: 0px;'
            'margin: 0px;'
            '}')

    @staticmethod
    def headerbar_margin() -> tuple:
        """..."""
        return 0, 0, 0, 0

    @staticmethod
    def windowcontrolbutton_margin() -> tuple:
        """..."""
        return 0, 0, 0, 0

    @staticmethod
    def windowcontrolbutton_spacing() -> int:
        """..."""
        return 0

    @staticmethod
    def window_border() -> int:
        """..."""
        return 1

    def window_border_color(self) -> QtGui.QColor:
        """..."""
        if self.window_is_dark():
            return color.rgba_to_qcolor(
                color.lighten_rgba(
                    self.palette.color(QtGui.QPalette.Window).to_tuple(), 15))

        return color.rgba_to_qcolor(color.darken_rgba(
            self.palette.color(QtGui.QPalette.Window).to_tuple(), 50))

    @staticmethod
    def window_border_radius() -> tuple:
        """..."""
        return 8, 8, 0, 0

    @staticmethod
    def window_icon_margin() -> tuple:
        """..."""
        return 5, 5, 5, 5
