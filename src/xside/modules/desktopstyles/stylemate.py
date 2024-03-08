#!/usr/bin/env python3
import logging

from PySide6 import QtGui
from __feature__ import snake_case

import xside.modules.desktopstyles.stylexfce as stylexfce


class EnvStyleMate(stylexfce.EnvStyleXFCE):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)

    def contextmenu_border_color(self) -> QtGui.QColor:
        """..."""
        if self.window_is_dark():
            return QtGui.QColor(80, 80, 80, 255)
        return QtGui.QColor(180, 180, 180, 255)

    def contextmenu_border_radius(self) -> int:
        """..."""
        return self.window_border_radius()[0]

    def contextmenu_separator_color(self) -> QtGui.QColor:
        """..."""
        if self.window_is_dark():
            return QtGui.QColor(80, 80, 80, 255)
        return QtGui.QColor(200, 200, 200, 255)

    def contextmenubutton_background_hover_color(self) -> QtGui.QColor:
        """..."""
        if self.window_is_dark():
            return QtGui.QColor(62, 62, 62, 255)
        return QtGui.QColor(222, 222, 222, 255)

    def contextmenubutton_border_hover_color(self) -> QtGui.QColor:
        """..."""
        return self.contextmenubutton_background_hover_color()

    @staticmethod
    def contextmenubutton_border_radius() -> int:
        """..."""
        return 0

    def contextmenubutton_label_hover_color(self) -> QtGui.QColor:
        """..."""
        return self.label_color()

    @staticmethod
    def controlbutton_style(*args, **kwargs) -> str:
        logging.info(args)
        logging.info(kwargs)

        """..."""
        return (
            'ControlButton {'
            '  border: 0px;'
            '  border-radius: 10px;'
            '  background-color: rgba(127, 127, 127, 0.2);'
            '  margin: 3px 4px 3px 4px;'
            '  padding: 1px 0px 0px 1px;'
            '}'
            'ControlButton:hover {'
            '  background-color: rgba(127, 127, 127, 0.3);'
            '}')
