#!/usr/bin/env python3
from PySide6 import QtGui, QtWidgets
from __feature__ import snake_case


class QQuickContextMenuSeparator(QtWidgets.QFrame):
    """..."""
    def __init__(self, top_level: QtWidgets, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__top_level = top_level
        self.__bd_color = self.__top_level.palette().color(
            QtGui.QPalette.Window.Mid)

        self.set_frame_shape(QtWidgets.QFrame.HLine)
        self.set_frame_shadow(QtWidgets.QFrame.Plain)
        self.set_line_width(0)
        self.set_mid_line_width(3)
        self.set_contents_margins(0, 0, 0, 0)
        self.set_color(color=QtGui.QColor(self.__bd_color))

    def set_color(self, color: QtGui.QColor) -> None:
        """..."""
        palette = self.palette()
        palette.set_color(QtGui.QPalette.WindowText, color)
        self.set_palette(palette)
