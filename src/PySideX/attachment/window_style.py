#!/usr/bin/env python3
import os

from PySide6 import QtGui, QtWidgets
from __feature__ import snake_case


class DynamicStyle(object):
    """..."""
    def __init__(self, main_window: QtWidgets.QMainWindow) -> None:
        """..."""
        self.__main_window = main_window
        self.__src = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        self.__bd_radius = self.__main_window.platform().window_border_radius()
        self.__bg_color = self.__main_window.palette().color(
            QtGui.QPalette.Window)
        self.__bd_color = self.__main_window.palette().color(
            QtGui.QPalette.Window.Mid)
        # https://doc.qt.io/qtforpython-6/PySide6/QtGui/
        # QPalette.html#PySide6.QtGui.PySide6.QtGui.QPalette.ColorGroup

    def build_style(self) -> str:
        """..."""

        if not self.__bd_radius:
            self.__bd_radius = 10, 10, 3, 3

        if self.__main_window.decoration():
            main_window_style = (
                '#QMainWindowCSD {' +
                'background-color: rgba({}, {}, {}, {});'.format(
                    self.__bg_color.red(), self.__bg_color.green(),
                    self.__bg_color.blue(), self.__bd_color.alpha_f()) +
                '}')
        else:
            main_window_style = (
                '#QMainWindowCSD {' +
                'background-color: rgba({}, {}, {}, {});'.format(
                    self.__bg_color.red(), self.__bg_color.green(),
                    self.__bg_color.blue(), self.__bd_color.alpha_f()) +
                'border: 1px solid rgba({}, {}, {}, {});'.format(
                    self.__bd_color.red(), self.__bd_color.green(),
                    self.__bd_color.blue(), self.__bd_color.alpha_f()) +
                f'border-top-left-radius: {self.__bd_radius[0]};' +
                f'border-top-right-radius: {self.__bd_radius[1]};' +
                f'border-bottom-right-radius: {self.__bd_radius[2]};' +
                f'border-bottom-left-radius: {self.__bd_radius[3]};' +
                '}')

        style_path = os.path.join(
            self.__src.replace('attachment', 'style'), 'style.qss')
        with open(style_path, 'r') as style_qss_file:
            style = style_qss_file.read()

        return main_window_style + style

    @staticmethod
    def adapt_style_to_max(style: str) -> str:
        # ...
        central_widget = [
            x for x in style.split('}') if
            x.strip().startswith(f'#QMainWindowCSD')][-1]

        return style.replace(
            central_widget, central_widget + 'border-radius: 0px; border: 0px')
