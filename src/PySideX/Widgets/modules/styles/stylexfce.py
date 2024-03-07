#!/usr/bin/env python3
import logging

from PySide6 import QtGui
from __feature__ import snake_case

import PySideX.Widgets.modules.color as color
import PySideX.Widgets.modules.styles.style as style


class EnvStyleXFCE(style.EnvStyle):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)

    @staticmethod
    def contextmenu_bg_alpha() -> float:
        """..."""
        return 1.0

    def contextmenu_border_color(self) -> QtGui.QColor:
        """..."""
        if self.window_is_dark():
            return QtGui.QColor(50, 50, 50, 255)
        return QtGui.QColor(180, 180, 180, 255)

    def contextmenubutton_border_hover_color(self) -> QtGui.QColor:
        """..."""
        return color.rgba_to_qcolor(
            color.darken_rgba(self.window_accent_color().to_tuple(), 50))

    @staticmethod
    def contextmenubutton_label_hover_color() -> QtGui.QColor:
        """..."""
        return QtGui.QColor(255, 255, 255, 255)

    @staticmethod
    def contextmenu_border_radius() -> int:
        """..."""
        return 0

    @staticmethod
    def contextmenu_padding() -> tuple:
        """..."""
        return 1, 6, 1, 6

    def contextmenu_separator_color(self) -> QtGui.QColor:
        """..."""
        if self.window_is_dark():
            return QtGui.QColor(50, 50, 50, 255)
        return QtGui.QColor(180, 180, 180, 255)

    @staticmethod
    def contextmenu_separator_margin() -> tuple:
        """Left, top, right and bottom margins tuple"""
        return 1, 0, 1, 0

    @staticmethod
    def contextmenubutton_bg_hover_alpha() -> float:
        """..."""
        return 1.0

    @staticmethod
    def contextmenubutton_padding() -> tuple:
        """..."""
        return 2, 4, 2, 4

    @staticmethod
    def contextmenugroup_padding() -> tuple:
        """..."""
        return 2, 4, 2, 6

    @staticmethod
    def controlbutton_order() -> tuple:
        """XAI M -> (2, 1, 0), (3,)

        Close     Max       Min       Icon      Above all
        X = 2     A = 1     I = 0     M = 3     F = 4

        (2, 1, 0), (3,) -> [Close Max Min ............. Icon]
        """
        return (3,), (0, 1, 2)

    @staticmethod
    def controlbutton_style(*args, **kwargs) -> str:
        logging.info(args)
        logging.info(kwargs)

        """..."""
        return (
            'ControlButton {'
            '  border: 0px;'
            '  border-radius: 3px;'
            '  margin: 0px;'
            '  padding: 1px;'
            '}'
            'ControlButton:hover {'
            '  background-color: rgba(127, 127, 127, 0.2);'
            '}')

    def window_border_color(self) -> QtGui.QColor:
        """..."""
        if self.window_is_dark():
            return color.rgba_to_qcolor(
                color.lighten_rgba(
                    self.palette.color(QtGui.QPalette.Window).to_tuple(), 30))

        return color.rgba_to_qcolor(color.darken_rgba(
            self.palette.color(QtGui.QPalette.Window).to_tuple(), 60))

    @staticmethod
    def window_border_radius() -> tuple:
        """..."""
        return 8, 8, 0, 0
