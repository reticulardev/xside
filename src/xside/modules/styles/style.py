#!/usr/bin/env python3
import logging

from PySide6 import QtGui
from __feature__ import snake_case

import xside.modules.color as color


class Main(object):
    def __init__(self, *args, **kwargs):
        self.palette = QtGui.QPalette()


class EnvStyle(Main):
    """Base environment settings"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def contextmenu_background_color(self) -> QtGui.QColor:
        """..."""
        return self.window_background_color()

    def contextmenu_border_color(self) -> QtGui.QColor:
        """..."""
        return self.window_border_color()

    def contextmenu_border_radius(self) -> int:
        """..."""
        return self.window_border_radius()[0]

    @staticmethod
    def contextmenu_margin() -> tuple:
        """..."""
        return 0, 0, 0, 0

    @staticmethod
    def contextmenu_padding() -> tuple:
        """..."""
        return 4, 4, 4, 4

    def contextmenu_separator_color(self) -> QtGui.QColor:
        """..."""
        return self.window_border_color()

    @staticmethod
    def contextmenu_separator_margin() -> tuple:
        """Left, top, right and bottom margins tuple"""
        return 0, 4, 0, 4

    @staticmethod
    def contextmenu_spacing() -> int:
        """..."""
        return 0

    def contextmenubutton_background_hover_color(self) -> QtGui.QColor:
        """..."""
        return self.window_accent_color()

    def contextmenubutton_border_hover_color(self) -> QtGui.QColor:
        """..."""
        return self.window_accent_color()

    def contextmenubutton_border_radius(self) -> int:
        """..."""
        contextmenu_bdr = self.contextmenu_border_radius()
        return contextmenu_bdr - 4 if contextmenu_bdr > 4 else contextmenu_bdr

    def contextmenubutton_label_hover_color(self) -> QtGui.QColor:
        """..."""
        return self.label_color()

    @staticmethod
    def contextmenubutton_padding() -> tuple:
        """..."""
        return 4, 6, 4, 6

    @staticmethod
    def contextmenugroup_padding() -> tuple:
        """..."""
        return 0, 6, 0, 8

    @staticmethod
    def controlbutton_order() -> tuple:
        """XAI M -> (2, 1, 0), (3,)

        Close     Max       Min       Icon      Above all
        X = 2     A = 1     I = 0     M = 3     F = 4

        (2, 1, 0), (3,) -> [Close Max Min ............. Icon]
        """
        return (2, 1, 0), (3,)

    @staticmethod
    def controlbutton_style(*args, **kwargs) -> str:
        logging.info(args)
        logging.info(kwargs)
        """..."""
        return (
            'ControlButton {'
            '  border: 0px;'
            '  border-radius: 10px;'
            '  padding: 1px;'
            '  background-color: rgba(127, 127, 127, 0.2);'
            '}'
            'ControlButton:hover {'
            '  background-color: rgba(200, 200, 200, 0.2);'
            '}')

    @staticmethod
    def desktop_is_using_global_menu() -> bool:
        """..."""
        return False

    @staticmethod
    def headerbar_margin() -> tuple:
        """..."""
        return 4, 4, 4, 4

    @staticmethod
    def icon_theme_name() -> str:
        """..."""
        return 'hicolor'

    def label_color(self) -> QtGui.QColor:
        """..."""
        return self.palette.color(
            QtGui.QPalette.Active, QtGui.QPalette.WindowText)

    def label_context_color(self) -> QtGui.QColor:
        """..."""
        return self.label_disabled_color()

    def label_disabled_color(self) -> QtGui.QColor:
        """..."""
        return self.palette.color(
            QtGui.QPalette.Disabled, QtGui.QPalette.WindowText)

    @staticmethod
    def windowcontrolbutton_margin() -> tuple:
        """..."""
        return 2, 0, 2, 0

    @staticmethod
    def windowcontrolbutton_spacing() -> int:
        """..."""
        return 6

    def window_accent_color(self) -> QtGui.QColor:
        """..."""
        return self.palette.color(
            QtGui.QPalette.Active, QtGui.QPalette.Highlight)

    def window_background_color(self) -> QtGui.QColor:
        """..."""
        return self.palette.color(QtGui.QPalette.Window)

    def window_background_darker_color(self) -> QtGui.QColor:
        """..."""
        step = 4 if self.window_is_dark() else 10
        return color.rgba_to_qcolor(color.darken_rgba(
            self.window_background_color().to_tuple(), step))

    def window_background_lighter_color(self) -> QtGui.QColor:
        """..."""
        step = 4 if self.window_is_dark() else 5
        return color.rgba_to_qcolor(color.lighten_rgba(
            self.window_background_color().to_tuple(), step))

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
            self.palette.color(QtGui.QPalette.Window).to_tuple(), 30))

    @staticmethod
    def window_border_radius() -> tuple:
        """..."""
        return 5, 5, 5, 5

    def window_is_dark(self) -> bool:
        """..."""
        return color.is_dark(self.window_background_color().to_tuple())

    @staticmethod
    def window_margin() -> tuple:
        """..."""
        return 0, 0, 0, 0

    @staticmethod
    def window_icon_margin() -> tuple:
        """..."""
        return 1, 0, 1, 0
